
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# On importe l'app SANS déclencher le pipeline main.py
from api.api import app

client = TestClient(app)


# HELPER : récupérer un token valide pour les routes protégées

def get_token():
    response = client.post("/token", data={
        "username": "lucas",
        "password": "oceluc"
    })
    return response.json()["access_token"]



# TESTS : Authentification

def test_login_succes():
    """Un bon login renvoie un token."""
    response = client.post("/token", data={
        "username": "lucas",
        "password": "oceluc"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_mauvais_mot_de_passe():
    """Un mauvais mot de passe renvoie 400."""
    response = client.post("/token", data={
        "username": "lucas",
        "password": "mauvais"
    })
    assert response.status_code == 400


def test_login_utilisateur_inconnu():
    """Un utilisateur inexistant renvoie 400."""
    response = client.post("/token", data={
        "username": "inconnu",
        "password": "oceluc"
    })
    assert response.status_code == 400



# TESTS : Routes protégées (vins / plats)

def test_get_vins_sans_token():
    """Sans token, on doit avoir 401."""
    response = client.get("/vins")
    assert response.status_code == 401


def test_get_vins_avec_token():
    """Avec un token valide, la route /vins répond."""
    token = get_token()
    with patch("api.api.get_db_connection") as mock_conn:
        # On simule une BDD qui renvoie une liste vide
        mock_conn.return_value.execute.return_value.fetchall.return_value = []
        mock_conn.return_value.close = MagicMock()

        response = client.get("/vins", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_get_plats_sans_token():
    """Sans token, on doit avoir 401."""
    response = client.get("/plats")
    assert response.status_code == 401



# TESTS : Route IA (libre, sans token)

def test_sommelier_chat():
    """La route /sommelier/chat répond sans token."""
    with patch("api.api.bacchus_agent") as mock_agent:
        # On simule la réponse de l'agent IA
        mock_msg = MagicMock()
        mock_msg.content = "Je vous recommande un Bordeaux."
        mock_agent.invoke.return_value = {"messages": [mock_msg]}

        response = client.post(
            "/sommelier/chat",
            params={"message": "Quel vin avec un poulet rôti ?"}
        )
        assert response.status_code == 200
        assert "response" in response.json()



# TESTS : Frigo

def test_get_frigo():
    """La route /frigo répond avec une liste."""
    with patch("api.api.mon_frigo") as mock_frigo:
        mock_frigo.contenu = []  # frigo vide
        response = client.get("/frigo")
        assert response.status_code == 200
        assert isinstance(response.json(), list)