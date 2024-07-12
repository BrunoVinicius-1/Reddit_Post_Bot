import praw
from reddit_funcoes import post_to_subreddit
from reddit_funcoes import get_oauth_code

#   	to do
# -- login por usuario e senha é melhor!
# -- criar um layout para o app
# -- importar flair dos subreddits para um checkbox
# -- definir titulo, imagens, flairs, comentarios como default e salvar para outros usos
# -- monitoramento de horario para postar diariamente só executando o script


# Reddit configuração
client_id='EzdZ8aVAY_sBIZ_fICHuUw'
client_secret='wdzKBqfwKf3QonaVV8SFAIN5tiRVYPxA' #tu consegue na aba app do reddit
redirect_uri = 'http://localhost:8080' # localhost normal
user_agent = 'u/BvvbArt'

reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        user_agent=user_agent,
    )

#código de autorização OAuth
auth_code = get_oauth_code(reddit, client_id, redirect_uri)

# Lista de subreddits
#subreddits = ['artcommission', 'hireanartist', 'dndcommissions', 'gameDevJobs', 'Artistsforhire', 'tabletopartists', 'commissions']
subreddits = ['gameDevJobs']

# Dicionario com cada flair que vai usar
subreddit_flairs = {
    'gameDevJobs': 'FOR HIRE - 2D Art | Animation',
    'artcommission': 'For Hire', 
    'hireanartist': '[FOR HIRE] - artist', 
    'dndcommissions': 'Comm',  
    'Artistsforhire': 'For Hire - Artist', 
    'tabletopartists': '', 
    'commissions': '[FOR HIRE]',
}

#subreddits_N_Diarios = [
    # 'starvingartists': '', 
    # 'HungryArtists': 'Commissions Open', 
    # 'DnDart': 'Self-Post (Accepting Commisions)',
    # 'artcommissions': 'Artist',]

# Iterar sobre cada subreddit na lista
for subreddit_name in subreddits:
    post_to_subreddit(reddit, subreddit_name, subreddit_flairs)