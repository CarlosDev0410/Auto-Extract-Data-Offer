"""
Interface Gráfica Desktop - Gerador de Planilha Oferta Relâmpago
Interface moderna e cross-platform (Windows 11 e macOS)
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
import json
from datetime import datetime
from database import DatabaseConnection
from export_excel import ExcelExporter
from config import OUTPUT_FILENAME, SQL_FILE


class OfertaRellampagoGUI:
    """Interface gráfica moderna para geração de planilhas"""
    
    # Cores modernas (tema escuro)
    COLOR_BG = "#1e1e2e"
    COLOR_SURFACE = "#2a2a3e"
    COLOR_PRIMARY = "#6366f1"
    COLOR_PRIMARY_HOVER = "#4f46e5"
    COLOR_TEXT = "#e0e0e0"
    COLOR_TEXT_SECONDARY = "#a0a0a0"
    COLOR_SUCCESS = "#10b981"
    COLOR_ERROR = "#ef4444"
    
    METADATA_FILE = "last_extraction.json"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Oferta Relâmpago")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR_BG)
        
        # Configura ícone se existir
        try:
            # No Windows
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.setup_ui()
        self.load_last_extraction()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Container principal
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="⚡ OFERTA RELÂMPAGO",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Gerador de Planilha",
            font=("Segoe UI", 12),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Card para informações
        info_card = tk.Frame(main_frame, bg=self.COLOR_SURFACE, relief="flat")
        info_card.pack(fill="x", pady=(0, 25))
        
        # Label de última extração
        self.last_extraction_label = tk.Label(
            info_card,
            text="Última extração: Nunca",
            font=("Segoe UI", 11),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_TEXT_SECONDARY,
            pady=15
        )
        self.last_extraction_label.pack()
        
        # Botão principal
        self.download_button = tk.Button(
            main_frame,
            text="📥 BAIXAR PLANILHA OFERTA",
            font=("Segoe UI", 14, "bold"),
            bg=self.COLOR_PRIMARY,
            fg="white",
            activebackground=self.COLOR_PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.start_download,
            height=2,
            bd=0,
            highlightthickness=0
        )
        self.download_button.pack(fill="x", ipady=10)
        
        # Efeito hover no botão
        self.download_button.bind("<Enter>", self.on_button_hover)
        self.download_button.bind("<Leave>", self.on_button_leave)
        
        # Label de status
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_SECONDARY
        )
        self.status_label.pack(pady=(15, 0))
        
        # Barra de progresso (inicialmente oculta)
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        
        # Estilo da barra de progresso
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "TProgressbar",
            troughcolor=self.COLOR_SURFACE,
            background=self.COLOR_PRIMARY,
            borderwidth=0,
            thickness=4
        )
        
        # Área de log
        log_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        log_frame.pack(fill="both", expand=True, pady=(15, 0))
        
        log_label = tk.Label(
            log_frame,
            text="📋 Log de Extração",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        log_label.pack(anchor="w", pady=(0, 5))
        
        # Widget de texto para logs (com scroll)
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_TEXT_SECONDARY,
            insertbackground=self.COLOR_TEXT,
            relief="flat",
            wrap=tk.WORD,
            state="disabled",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.log_text.pack(fill="both", expand=True)
    
    def on_button_hover(self, event):
        """Efeito hover no botão"""
        self.download_button.config(bg=self.COLOR_PRIMARY_HOVER)
    
    def on_button_leave(self, event):
        """Remove efeito hover"""
        self.download_button.config(bg=self.COLOR_PRIMARY)
    
    def load_last_extraction(self):
        """Carrega informação da última extração"""
        try:
            if os.path.exists(self.METADATA_FILE):
                with open(self.METADATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    last_date = data.get('last_extraction')
                    if last_date:
                        dt = datetime.fromisoformat(last_date)
                        formatted_date = dt.strftime("%d/%m/%Y às %H:%M")
                        self.last_extraction_label.config(
                            text=f"📅 Última extração: {formatted_date}"
                        )
        except Exception as e:
            print(f"Erro ao carregar última extração: {e}")
    
    def save_last_extraction(self):
        """Salva a data/hora da última extração bem-sucedida"""
        try:
            data = {
                'last_extraction': datetime.now().isoformat()
            }
            with open(self.METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar última extração: {e}")
    
    def log_message(self, message, clear=False):
        """
        Adiciona uma mensagem ao log
        
        Args:
            message: Mensagem a ser adicionada
            clear: Se True, limpa o log antes de adicionar
        """
        def update_log():
            self.log_text.config(state="normal")
            if clear:
                self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)  # Auto-scroll
            self.log_text.config(state="disabled")
        
        self.root.after(0, update_log)
    
    def start_download(self):
        """Inicia o processo de download em uma thread separada"""
        # Limpa o log anterior
        self.log_message("", clear=True)
        
        # Desabilita o botão durante o processamento
        self.download_button.config(state="disabled", bg=self.COLOR_TEXT_SECONDARY)
        self.status_label.config(text="⏳ Processando...", fg=self.COLOR_TEXT)
        self.progress.pack(pady=(10, 0))
        self.progress.start(10)
        
        # Executa em thread para não travar a UI
        thread = threading.Thread(target=self.download_spreadsheet, daemon=True)
        thread.start()
    
    def download_spreadsheet(self):
        """Executa o processo de extração e geração da planilha"""
        try:
            self.log_message("🚀 Iniciando processo de extração...")
            
            # Carrega a query SQL
            self.log_message("📄 Carregando query SQL...")
            with open(SQL_FILE, 'r', encoding='utf-8') as f:
                query = f.read()
            
            # Conecta ao banco e executa query
            self.log_message("🔌 Conectando ao banco de dados...")
            with DatabaseConnection() as db:
                if not db.connection:
                    self.log_message("❌ Falha na conexão com o banco de dados")
                    self.show_error("Erro ao conectar ao banco de dados.\nVerifique suas credenciais no arquivo .env")
                    return
                
                self.log_message("✅ Conectado com sucesso!")
                self.log_message("🔍 Consultando dados...")
                
                # Executa a query
                df = db.execute_query(query)
                
                if df is None or df.empty:
                    self.log_message("⚠️ Nenhum dado retornado pela query")
                    self.show_error("Nenhum dado foi retornado pela query.")
                    return
                
                self.log_message(f"✅ {len(df)} registros encontrados!")
            
            self.log_message("📊 Extraindo dados...")
            
            # Pergunta onde salvar o arquivo
            self.log_message("💾 Aguardando seleção do local de salvamento...")
            file_path = self.ask_save_location()
            
            if not file_path:
                self.log_message("⚠️ Operação cancelada pelo usuário")
                self.reset_ui()
                return
            
            self.log_message(f"💾 Salvando em: {file_path}")
            
            # Exporta para Excel
            success = ExcelExporter.export_data(df, file_path)
            
            if success:
                self.log_message("✅ Planilha gerada com sucesso!")
                self.save_last_extraction()
                self.show_success(f"Planilha gerada com sucesso!\n\n📁 {file_path}")
                self.load_last_extraction()
            else:
                self.log_message("❌ Erro ao gerar planilha")
                self.show_error("Falha ao gerar planilha.")
        
        except FileNotFoundError:
            self.log_message(f"❌ Arquivo {SQL_FILE} não encontrado")
            self.show_error(f"Arquivo {SQL_FILE} não encontrado!")
        except Exception as e:
            self.log_message(f"❌ Erro: {str(e)}")
            self.show_error(f"Erro inesperado:\n{str(e)}")
    
    def ask_save_location(self):
        """Abre dialog para usuário escolher onde salvar o arquivo"""
        def show_dialog():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=OUTPUT_FILENAME,
                title="Salvar planilha como"
            )
            self.selected_file_path = file_path
        
        # Executa na thread principal
        self.selected_file_path = None
        self.root.after(0, show_dialog)
        
        # Aguarda a seleção
        while self.selected_file_path is None:
            import time
            time.sleep(0.1)
        
        return self.selected_file_path
    
    def reset_ui(self):
        """Reseta a interface para o estado inicial"""
        def _reset():
            self.progress.stop()
            self.progress.pack_forget()
            self.status_label.config(text="")
            self.download_button.config(state="normal", bg=self.COLOR_PRIMARY)
        
        self.root.after(0, _reset)
    
    def show_success(self, message):
        """Mostra mensagem de sucesso"""
        self.root.after(0, lambda: self._show_success_ui(message))
    
    def _show_success_ui(self, message):
        """Atualiza UI com mensagem de sucesso (executa na thread principal)"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="✅ Concluído!", fg=self.COLOR_SUCCESS)
        self.download_button.config(state="normal", bg=self.COLOR_PRIMARY)
        messagebox.showinfo("Sucesso", message)
        self.status_label.config(text="")
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        self.root.after(0, lambda: self._show_error_ui(message))
    
    def _show_error_ui(self, message):
        """Atualiza UI com mensagem de erro (executa na thread principal)"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="❌ Erro!", fg=self.COLOR_ERROR)
        self.download_button.config(state="normal", bg=self.COLOR_PRIMARY)
        messagebox.showerror("Erro", message)
        self.status_label.config(text="")


def main():
    """Função principal"""
    root = tk.Tk()
    app = OfertaRellampagoGUI(root)
    
    # Centraliza a janela na tela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
