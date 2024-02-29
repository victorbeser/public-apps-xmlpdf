
##########################################################################
#                                                                        #   
#   Desenvolvido por:                                                    #   
#                                                                        #   
#           V          V  III CCCCCC   TTTTTTTTT OOOOOO RRRRRR           #
#           V          V   I  C           T     O    O  R    R           #   
#            V        V    I  C           T     O    O  R    R           #  
#            V        V    I  C           T     O    O  RRRRR            #   
#             V      V     I  C           T     O    O  R   R            #   
#             V      V     I  C           T     O    O  R    R           #   
#              V    V      I  C           T     O    O  R     R          #   
#               V  V      III CCCCCC      T    OOOOOOO  R      R         #   
#                                                                        #   
#                            BBBBB    EEEEE   SSSS   EEEEE  RRRRR        #   
#                            B    B   E       S      E      R    R       #   
#                            BBBBB    EEEE     SSS   EEEE   RRRRR        #   
#                            B    B   E           S  E      R  R         #   
#                            BBBBB    EEEEE   SSSS   EEEEE  R   R        #   
#                                                                        #   
#                                                TikTok: @victorbeser    #   
#                                                Instagram: @jvbeesan    #   
#                                                                        #   
##########################################################################



# BIBLIOTECAS QUE VOCÊ DEVE INSTALAR PARA RODAR O APP
import tkinter as tk
from tkinter import filedialog, messagebox
from fpdf import FPDF
import xml.etree.ElementTree as ET


# Inicio do APP
class XMLtoPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor XML para PDF - TikTok @victorbeser")
        self.root.geometry("400x200") 

        self.label_xml = tk.Label(root, text="Arquivo XML selecionado:")
        self.label_xml.pack()

        self.selected_xml_label = tk.Label(root, text="")
        self.selected_xml_label.pack()

        self.btn_xml = tk.Button(root, text="Selecionar XML", command=self.select_xml_file)
        self.btn_xml.pack()

        self.label_output = tk.Label(root, text="Pasta de saída:")
        self.label_output.pack()

        self.selected_output_label = tk.Label(root, text="")
        self.selected_output_label.pack()

        self.btn_output = tk.Button(root, text="Selecionar Pasta", command=self.select_output_location)
        self.btn_output.pack()

        self.btn_convert = tk.Button(root, text="Converter para PDF", command=self.convert_to_pdf)
        self.btn_convert.pack()


    # Func pra selecionar o arquivo XML
    def select_xml_file(self):
        self.xml_path = filedialog.askopenfilename(title="Selecione o arquivo XML")
        self.selected_xml_label.config(text=self.xml_path)
    
    # Func pra selecionar a pasta de output em PDF
    def select_output_location(self):
        self.output_folder = filedialog.askdirectory(title="Selecione a pasta de saída")
        self.selected_output_label.config(text=self.output_folder)

    # Func que faz a conversao
    def convert_to_pdf(self):
        if not hasattr(self, 'xml_path') or not hasattr(self, 'output_folder'):
            messagebox.showerror("Erro", "Por favor, selecione tanto o arquivo XML quanto a pasta de saída.")
            return

        informacoes_nota = self.extract_information_from_xml(self.xml_path)
        pdf_path = self.output_folder + "/nota_fiscal.pdf"
        self.create_pdf(informacoes_nota, pdf_path)
        messagebox.showinfo("Conversão Concluída", "A nota fiscal foi convertida para PDF com sucesso!")

    # Extrair infos do XML
    def extract_information_from_xml(self, xml_path):
        informacoes = {}
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for child in root:
            if child.tag == 'produtos':
                informacoes[child.tag] = []
                for produto in child:
                    produto_info = {}
                    for info in produto:
                        produto_info[info.tag] = info.text
                    informacoes[child.tag].append(produto_info)
            else:
                informacoes[child.tag] = child.text

        return informacoes

    # Criar PDF com as infos do XML
    def create_pdf(self, informacoes, pdf_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for chave, valor in informacoes.items():
            if isinstance(valor, list):  # Se for uma lista (produtos)
                pdf.cell(200, 10, txt=f"{chave}:", ln=True, align='L')
                for produto in valor:
                    for produto_chave, produto_valor in produto.items():
                        pdf.cell(200, 10, txt=f"{produto_chave}: {produto_valor}", ln=True, align='L')
            else:
                pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True, align='L')

        pdf.output(pdf_path)


def main():
    root = tk.Tk()
    app = XMLtoPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
