import praw
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


def get_oauth_code(reddit, client_id, redirect_uri):
    """
    Abre o navegador para o usuário autorizar e obtém o código de autorização.

    :client_id: ID do cliente do Reddit.
    :redirect_uri: URI de redirecionamento para a autenticação.
    :return: Código de autorização.
    """
    # autenticação
    oauth_url = f'https://www.reddit.com/api/v1/authorize?client_id={client_id}&response_type=code&state=some_random_state&redirect_uri={redirect_uri}&duration=permanent&scope=identity,submit,wikiread,wikiedit,flair'
    
    # Abre o navegador para o usuário autorizar
    webbrowser.open(oauth_url)

    # HTTP p/ pegar o código de autorização
    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            query = parse_qs(parsed_path.query)
            if 'code' in query:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Recebi o codigo de autorizacao. Pode fechar esta aba.')
                self.server.auth_code = query['code'][0]

    server = HTTPServer(('localhost', 8080), OAuthHandler)
    server.handle_request()
    auth_code = server.auth_code
    
    # Obtendo o token de atualização usando o código de autorização
    try:
            refresh_token = reddit.auth.authorize(auth_code)
    except Exception as e:
            print(f"Erro ao obter o refresh token: {e}")


    return None

def post_to_subreddit(reddit, subreddit_name, subreddit_flairs):
    """
    Posta na galeria de imagens em um subreddit com um flair específico.

    :reddit: Instância autenticada do Reddit.
    :subreddit_name: Nome do subreddit onde a postagem será feita.
    :subreddit_flairs: Dicionário com os flairs de cada subreddit.
    """
    
    # Subreddit onde você quer fazer a postagem
    subreddit = reddit.subreddit("subreddit_name")

    # Postar texto e filtrar pro subreddit fdp que criaram com a bunda e erraram a porra do for hire
    if subreddit == 'comissions':
        post_title = "[Foe Hire] Do you want art of your character? I'll do it for you, info in my carrd, Dm Open!!!"
    else:
        post_title = "[For Hire] Do you want art of your character? I'll do it for you, info in my carrd, Dm Open!!!"


    # Lista de imagens com caminhos e legendas 
    # futuramente planejo deixar o usuario importar as imagens no layout e manter salvo elas, mas por enquanto vai assim
    image_paths = ['Arts/minotauro.1.png', "Arts/arkh.jpg", "Arts/Tiefling.5.0.png"]
    images = [{'image_path': image_path, 'caption': f'Legenda {index + 1}'} for index, image_path in enumerate(image_paths)]

    # Post as imagens
    gallery_images = [{'image_path': image['image_path'], 'caption': image['caption']} for image in images]
    print("Postagem de galeria de imagens feita com sucesso!")
#-------------------------------------------------------------------------------------Área em Manutenção-------------------------------------------------------------------------------
    '''
    # Pegar ID da flair
    flair_id = None
    for flair in subreddit.flair.link_templates:
        if flair['text'] == subreddit_flairs[subreddit_name]:
            flair_id = flair['id']
            break

    if not flair_id:
        raise ValueError("Flair não encontrado")
    '''
    # arrumar codigo de importar as flairs do subreddit e permitir o usuario a escolher
    # Exibir flairs 
    print("Escolha uma flair:")
    flairs = reddit.subreddit(subreddit_name).flair
    print(flairs)
    try:
        for flair in flairs:
            print(flair)
    except praw.exceptions.APIException as e:
        print(f"Erro ao acessar flairs: {e}")
  

#---------------------------------------------------------------------------------------Não entre----------------------------------------------------------------------------------------------
    # Postar as imagens com o flair
    post = subreddit.submit_gallery(post_title, images=gallery_images, flair_id=flair_id)
    print("Postagem feita com sucesso!")

    # Comentar no post
    comment = post.reply("""Hello there (again)!!
    Commissions are open. (1 slot) I'll leave the link to my portfolio, prices and infos below so you can check if it's what you're looking for:
    
    Carrd: http://mestrecomissions.carrd.co/# 
    
    If interested, email me at bvvbmorais @ -- or in DM.""")

    if subreddit == 'Artistsforhire':
        time.sleep(10)

        #tem um subreddit que te obriga a comentar o preço, por isso essa merda
        # Responder a um comentário de um bot
        for comment in post.comments:
            if comment.author and comment.author.name == 'AutoModerator':
                comment.reply("""Portrait -> sketch: 10$, line art: 15$, full render: 45$

        Half Body -> sketch: 15$, line art: 30$, full render: 70$

        Full body -> sketch: 20$, line art: 45$, full render: 110$""")
            print("Resposta ao bot feita com sucesso!")