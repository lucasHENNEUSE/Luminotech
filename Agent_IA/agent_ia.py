import os
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain_groq import ChatGroq
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from ddgs import DDGS
from langchain_core.messages import HumanMessage, AIMessage

# --- IMPORT DE TON CODE CAPTEUR ---
# On importe l'outil que nous avons créé dans capteur.py
from capteur import consulter_inventaire_frigo

load_dotenv()   

# --- Configuration de l'Agent ---

SYSTEM_PROMPT = """Expert Sommelier et Chef (Bacchus IA). Style: chaleureux, expert.

## RÈGLES DE RÉPONSE
1. RECETTES & FRIGO : Si l'utilisateur demande quoi cuisiner ou ce qu'il y a dans son frigo, utilise TOUJOURS `consulter_inventaire_frigo`. Propose une recette avec les ingrédients détectés.
2. ACTION IMMÉDIATE : Réponds toujours à la question de l'utilisateur en proposant 2-3 vins, même si des détails manquent. Utilise `search_wine_web` pour garantir des références réelles.
3. STRUCTURE : 
   - Propose 2-3 bouteilles précises (prix variés).
   - Explique brièvement l'accord.
   - Donne un conseil de service (température/carafage).
4. RELANCE : Termine TOUJOURS par une seule question ouverte pour affiner (ex: budget, préférence de région, occasion).

## STYLE & ÉTHIQUE
- Pas de snobisme, pas de clichés ("robe rubis").
- Humour léger. 
- INTERDIT d'inventer des prix ou des vins.
- Rappel modération alcool. Pas de conseil médical.

## OUTILS
- Recherche web/prix/accords : utilise `search_wine_web`.
- Consultation du réfrigérateur : utilise `consulter_inventaire_frigo`.
"""

@tool
def search_wine_web(query: str) -> str:
    """Recherche des informations sur les vins via DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results]) if results else "Aucun résultat."
    except Exception as e:
        return f"Erreur : {str(e)}"
    
def call_bacchus(user_input, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        state = bacchus_agent.get_state(config)
        history = state.values.get("messages", [])[-4:] if state.values else []
        
        input_data = {"messages": history + [HumanMessage(content=user_input)]}
        
        response = bacchus_agent.invoke(input_data, config=config)
        
        return response["messages"][-1].content
        
    except Exception as e:
        print(f"ERREUR CRITIQUE AGENT : {e}")
        return "Bacchus a un petit bouchon... (Erreur technique). Réessaie dans un instant."

# Initialisation
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=2048, groq_api_key=os.getenv("GROQ_API_KEY"))
checkpointer = InMemorySaver()

@dataclass
class Context:
    user_id: str

# On exporte l'objet agent avec l'outil du frigo ajouté
bacchus_agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[search_wine_web, consulter_inventaire_frigo], # L'outil frigo est ici
    context_schema=Context,
    checkpointer=checkpointer
)