# Sistema de Relatórios de Exames e Consultas

## 📌 Descrição do Projeto
Este projeto foi desenvolvido com a biblioteca **CustomTkinter (CTkinter)** e outras bibliotecas auxiliares (Pandas, ReportLab, Tkinter, Pillow, etc.), com o objetivo de criar uma **plataforma completa de agendamento e geração de relatórios médicos**.  

O sistema auxilia o **profissional responsável pelos agendamentos médicos** em hospitais de Salvador, permitindo:
- Registrar pacientes e seus procedimentos (consultas, exames, cirurgias, resultados, medicamentos e retornos);
- Validar dados digitados (nome, telefone, data, horário, instituição, detalhamento do procedimento);
- Gerar relatórios completos em PDF, contendo estatísticas, tabelas e análises das atividades realizadas.

---

## ⚙️ Funcionalidades
- **Cadastro de Pacientes**: preenchimento de formulário com nome, telefone, procedimento, detalhamento, instituição, data, horário e envio.  
- **Autocompletar**:
  - Hospitais sugeridos a partir da lista de instituições aceitas.
  - Consultas sugeridas apenas quando o procedimento selecionado é "CONSULTA".
- **Validações**: 
  - Nome e telefone obrigatórios.
  - Datas no formato DD/MM/AAAA e horários válidos.
  - Instituição e consultas somente das listas pré-definidas.
- **Tratamento de Erros**: janelas explicativas caso algum campo seja preenchido incorretamente.
- **Gerenciamento de Dados**:
  - Salvar dados na base (Excel).
  - Excluir paciente cadastrado.
  - Limpar formulário.
  - Abrir relatórios já existentes.
- **Visualização**: exibição da base de dados em tabela interativa com barra de rolagem.  
- **Relatórios em PDF**:
  - Quantitativo geral de procedimentos.
  - Distribuição adulto/pediátrico.
  - Instituições mais utilizadas.
  - Consultas mais demandadas (TOP 5).
  - Tabela completa de pacientes.
- **Ajuda/Dúvidas**: guia rápido sobre uso do sistema.  

---

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **CustomTkinter (CTkinter)** → Interface gráfica moderna
- **Tkinter/ttk** → Elementos gráficos adicionais
- **Pandas** → Manipulação de dados
- **ReportLab** → Geração de relatórios em PDF
- **Pillow (PIL)** → Manipulação de imagens
- **Threading** → Execução assíncrona de geração de relatórios

---

## ▶️ Como Executar
1. Certifique-se de ter o Python 3 instalado.  
2. Instale as dependências necessárias (pip install customtkinter pandas reportlab pillow)
3. Execute o programa: python Exames_genérico.py (ou abra o arquivo executável na pasta do arquivo, que contém o programa em sua versão independente, feita com a biblioteca pyinstaller)
4. Utilize a interface para cadastrar pacientes, salvar dados e gerar relatórios.

---

## 📊 Público-Alvo
O sistema foi idealizado para apoiar **profissionais de marcação e regulação** em hospitais e clínicas de Salvador, oferecendo mais **agilidade, confiabilidade e organização** no processo de agendamento médico.

---

## 👨‍💻 Desenvolvedor
**Handrick Silveira**  
Estudante de Sistemas de Informação (Universidade de São Paulo)


