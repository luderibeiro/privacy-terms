import logging
import os

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fpdf import FPDF

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PDFGenerator(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Política de Privacidade", 0, 1, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, 0, 1, "L")

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        lines = body.split("\n")
        for line in lines:
            if line.startswith("**") and line.endswith("**"):
                self.set_font("Arial", "B", 12)
                line = line.strip("**")
            else:
                self.set_font("Arial", "", 12)
            self.cell(0, 10, line, ln=True)


@app.post("/privacy/generate")
def generate_privacy_policy(
    project_name: str = Form(...), contact_email: str = Form(...)
):
    try:
        pdf = PDFGenerator()
        pdf.add_page()
        pdf.chapter_title(f"Projeto: {project_name}")
        pdf.chapter_body("Política de Privacidade")

        privacy_policy_text = f"""
**POLÍTICA DE PRIVACIDADE**

**1. Introdução**
A presente Política de Privacidade descreve como o {project_name} coleta, usa e protege as 
informações pessoais dos usuários do aplicativo. Nosso compromisso é garantir que sua 
privacidade seja protegida. Se pedirmos que você forneça certas informações pelas quais você 
possa ser identificado ao usar este aplicativo, você pode ter certeza de que elas serão usadas 
apenas de acordo com esta declaração de privacidade.

**2. Informações Coletadas**
Coletamos informações pessoais que você nos fornece diretamente, como nome, e-mail, e outras
informações de contato. Além disso, podemos coletar informações sobre como você usa o aplicativo, 
incluindo dados sobre sua navegação e interações, para melhorar nossos serviços e personalizar sua 
experiência.

**3. Uso das Informações**
As informações coletadas são usadas para fornecer e melhorar os serviços do aplicativo, 
comunicar-se com você e personalizar sua experiência. Podemos também usar suas informações 
para fins de pesquisa interna, análise e auditoria para melhorar a funcionalidade do aplicativo 
e fornecer melhores serviços aos usuários.

**4. Compartilhamento de Informações**
Não compartilhamos suas informações pessoais com terceiros, exceto conforme necessário para 
fornecer nossos serviços ou conforme exigido por lei. Em certas situações, podemos ser obrigados 
a divulgar informações em resposta a solicitações legais de autoridades públicas, inclusive para 
cumprir requisitos de segurança nacional ou aplicação da lei.

**5. Segurança das Informações**
Implementamos medidas de segurança para proteger suas informações pessoais. No entanto, 
nenhuma medida de segurança é totalmente infalível. Empregamos diversas tecnologias e 
procedimentos de segurança para ajudar a proteger suas informações pessoais contra acesso, 
uso ou divulgação não autorizada.

**6. Seus Direitos**
Você tem o direito de acessar, corrigir e excluir suas informações pessoais, bem como de 
restringir ou se opor ao seu processamento. Para exercer esses direitos, você pode entrar em 
contato conosco através do e-mail fornecido, e responderemos a suas solicitações conforme 
exigido pelas leis aplicáveis.

**7. Contato**
Se você tiver alguma dúvida sobre esta Política de Privacidade, entre em contato conosco pelo 
e-mail: {contact_email}. Estamos disponíveis para esclarecer qualquer dúvida ou preocupação que 
você possa ter sobre nossas práticas de privacidade e a proteção de suas informações pessoais.

**8. Alterações a esta Política**
Reservamo-nos o direito de atualizar esta Política de Privacidade a qualquer momento. Notificaremos 
sobre quaisquer alterações publicando a nova política em nosso aplicativo. Recomendamos que você 
revise esta política periodicamente para se manter informado sobre como estamos protegendo suas 
informações.

**9. Consentimento**
Ao usar o aplicativo, você consente com a coleta e uso de suas informações conforme descrito nesta 
Política de Privacidade. Se não concordar com esta política, por favor, não use nosso aplicativo. O 
uso contínuo do aplicativo após a publicação de alterações a esta política será considerado como sua 
aceitação dessas alterações.

**10. Disposições Finais**
Se qualquer disposição desta política for considerada inválida, as demais disposições continuarão em 
pleno vigor e efeito. Esta política é regida e interpretada de acordo com as leis do país onde a sede do 
{project_name} está localizada, sem considerar os conflitos de provisões legais.

**11. LGPD - Lei Geral de Proteção de Dados**
A Lei Geral de Proteção de Dados (LGPD) é a legislação brasileira que regulamenta o tratamento 
de dados pessoais no Brasil. Esta seção detalha como o {project_name} se alinha com os 
requisitos da LGPD.

**11.1. Definição de Dados Pessoais**
A LGPD define dados pessoais como qualquer informação relacionada a uma pessoa natural 
identificada ou identificável. Isso inclui, mas não se limita a, nome, endereço, e-mail, 
número de telefone, dados de localização e identificadores online.

**11.2. Consentimento**
A coleta e o tratamento de dados pessoais são realizados com o consentimento explícito do titular 
dos dados, salvo exceções previstas na lei. O consentimento é fornecido de forma livre, 
informada e inequívoca.

**11.3. Direitos dos Titulares**
A LGPD garante aos titulares dos dados diversos direitos, incluindo o direito de acesso, correção, 
eliminação, portabilidade e a possibilidade de revogar o consentimento a qualquer momento. 
Os titulares também têm o direito de obter informações sobre o compartilhamento de seus dados 
com terceiros.

**11.4. Finalidade e Necessidade**
O tratamento de dados pessoais é realizado para atender a finalidades específicas, explícitas e 
legítimas, informadas ao titular dos dados. Além disso, é limitado ao mínimo necessário para a 
realização dessas finalidades.

**11.5. Segurança**
Implementamos medidas de segurança técnicas e administrativas adequadas para proteger os dados 
pessoais contra acessos não autorizados, situações acidentais ou ilícitas de destruição, perda, 
alteração, comunicação ou qualquer forma de tratamento inadequado ou ilícito.

**11.6. Responsabilidade e Prestação de Contas**
Os controladores de dados devem demonstrar conformidade com a LGPD, adotando medidas 
eficazes e apazes de comprovar a observância e o cumprimento das normas de proteção de dados.

**11.7. Transferência Internacional de Dados**
A transferência de dados pessoais para outros países só ocorre para países ou organismos 
internacionais que proporcionem um nível adequado de proteção de dados ou mediante o 
cumprimento de determinadas condições previstas na LGPD.

**11.8. Incidentes de Segurança**
A LGPD exige que notifiquemos a Autoridade Nacional de Proteção de Dados (ANPD) e os titulares 
dos dados em caso de incidentes de segurança que possam acarretar risco ou dano relevante aos 
titulares dos dados.

**11.9. Revisões e Atualizações**
Esta seção será revisada e atualizada periodicamente para garantir a conformidade contínua com 
a LGPD e qualquer nova legislação ou regulamentação aplicável.
        """

        pdf.chapter_body(privacy_policy_text.strip())

        output_path = f"{project_name}_privacy_policy.pdf"
        pdf.output(output_path)

        return FileResponse(
            output_path, media_type="application/pdf", filename=output_path
        )
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    logging.info("Starting server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
    )
