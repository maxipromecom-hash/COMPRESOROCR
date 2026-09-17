import os, threading
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from .processor import listar_imagenes, procesar_archivo

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Compresor OCR PRO')
        self.geometry('920x680')
        self.minsize(820, 600)
        self.folder = ctk.StringVar()
        self.api = ctk.StringVar(value=os.getenv('OCR_SPACE_API_KEY',''))
        self.ocr = ctk.BooleanVar(value=True)
        self.comp = ctk.BooleanVar(value=True)
        self.level = ctk.StringVar(value='Media')
        self._ui()

    def _ui(self):
        ctk.CTkLabel(self, text='COMPRESOR OCR PRO', font=ctk.CTkFont(size=28, weight='bold')).pack(pady=(22,4))
        ctk.CTkLabel(self, text='Comprime imágenes, reconoce Registros y renombra copias automáticamente').pack(pady=(0,18))
        box=ctk.CTkFrame(self); box.pack(fill='x', padx=24, pady=8)
        ctk.CTkEntry(box, textvariable=self.folder, placeholder_text='Seleccione una carpeta').pack(side='left', fill='x', expand=True, padx=12, pady=12)
        ctk.CTkButton(box, text='Examinar', command=self.examinar, width=120).pack(side='right', padx=12)
        opts=ctk.CTkFrame(self); opts.pack(fill='x', padx=24, pady=8)
        ctk.CTkCheckBox(opts,text='Reconocer Registro y renombrar',variable=self.ocr).grid(row=0,column=0,padx=16,pady=14,sticky='w')
        ctk.CTkCheckBox(opts,text='Comprimir imágenes',variable=self.comp).grid(row=0,column=1,padx=16,pady=14,sticky='w')
        ctk.CTkLabel(opts,text='Calidad:').grid(row=0,column=2,padx=(16,5))
        ctk.CTkOptionMenu(opts,values=['Alta','Media','Máxima compresión'],variable=self.level).grid(row=0,column=3,padx=8)
        api=ctk.CTkFrame(self); api.pack(fill='x', padx=24, pady=8)
        ctk.CTkLabel(api,text='OCR.space API key:').pack(side='left',padx=(14,8),pady=12)
        ctk.CTkEntry(api,textvariable=self.api,show='•').pack(side='left',fill='x',expand=True,padx=(0,14),pady=12)
        self.count=ctk.CTkLabel(self,text='0 imágenes detectadas'); self.count.pack(pady=(10,4))
        self.progress=ctk.CTkProgressBar(self); self.progress.pack(fill='x',padx=24,pady=8); self.progress.set(0)
        self.run=ctk.CTkButton(self,text='PROCESAR IMÁGENES',height=46,font=ctk.CTkFont(size=16,weight='bold'),command=self.iniciar); self.run.pack(fill='x',padx=24,pady=8)
        self.log=ctk.CTkTextbox(self); self.log.pack(fill='both',expand=True,padx=24,pady=(8,22)); self.log.insert('end','Los archivos originales no se modifican.\n')

    def examinar(self):
        d=filedialog.askdirectory()
        if d:
            self.folder.set(d); imgs=listar_imagenes(d); self.count.configure(text=f'{len(imgs)} imágenes detectadas'); self._log(f'Carpeta: {d}')

    def _log(self,s):
        self.log.insert('end',s+'\n'); self.log.see('end')

    def iniciar(self):
        if not self.folder.get() or not Path(self.folder.get()).is_dir(): return messagebox.showerror('Error','Seleccione una carpeta válida.')
        if self.ocr.get() and not self.api.get().strip(): return messagebox.showerror('API key','Ingrese su API key de OCR.space para reconocer Registros.')
        self.run.configure(state='disabled'); threading.Thread(target=self._procesar,daemon=True).start()

    def _procesar(self):
        imgs=listar_imagenes(self.folder.get()); out=Path(self.folder.get())/'IMAGENES_PROCESADAS'; out.mkdir(exist_ok=True)
        ok=sin=errores=0; antes=sum(p.stat().st_size for p in imgs)
        for i,p in enumerate(imgs,1):
            try:
                reg,dest,_=procesar_archivo(p,out,self.api.get().strip(),self.ocr.get(),self.comp.get(),self.level.get())
                ok+=1; sin += int(self.ocr.get() and not reg); self.after(0,self._log,f'[{i}/{len(imgs)}] {p.name} → {dest.name}' + ('' if reg or not self.ocr.get() else '  [SIN REGISTRO]'))
            except Exception as e:
                errores+=1; self.after(0,self._log,f'ERROR {p.name}: {e}')
            self.after(0,self.progress.set,i/max(len(imgs),1))
        despues=sum(p.stat().st_size for p in out.iterdir() if p.is_file())
        ahorro=max(0,antes-despues); pct=(ahorro/antes*100) if antes else 0
        msg=f'Finalizado. Procesadas: {ok} | Sin registro: {sin} | Errores: {errores} | Ahorro aprox.: {pct:.1f}%'
        self.after(0,self._log,msg); self.after(0,self.run.configure,state='normal'); self.after(0,messagebox.showinfo,'Proceso finalizado',msg+'\n\nSalida: '+str(out))
