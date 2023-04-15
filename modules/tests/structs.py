## Strip Foundation

class StripFoundation:
    standard_bar_length = 9.0
    length = 0
    width = 0
    depth = 0
    thickness = 0
    def __init__(self, data:dict=None):
        if data:
            self.data = data
            self.length = {'value': data.get('length'), 'unit': 'm'}
            self.width = {'value': data.get('width'), 'unit': 'm'}
            self.depth = {'value': data.get('depth'), 'unit': 'm'}
            self.thickness = {'value': data.get('thickness'), 'unit': 'm'} 
        else: 
            self.data = {}       
        self.main_bars = {
            "bar_type": "",
            "amount": 0,    
            "lap": 0

        }
        self.stirrup = {
            "bar_type": "",
            "amount": 0,
            "spacing": 0,
            "length": 0        

        }
        self.link = {
            "bar_type": "",
            "amount": 0,
            "spacing": 0,
            "length": 0            
        }

    # excavation
    def volume(self, len:float=None, width:float=None, depth:float=None ):
        return len * width * depth
    
    def set_volume(self):
        self.data['excavation'] = {
            "value": self.volume(len=self.data.get("length"), width=self.data.get('width'),depth=self.data.get('depth')),
            "unit": "m3"
            }

        self.data['concrete'] = {
                "dry_volume": self.volume(len=self.data.get("length"), width=self.data.get('width'),depth=self.data.get('thickness')),
                "wet_volume_constant": 1.54,
                "unit": "m3"
            }
        self.data["concrete"]["wet_volume"] = self.data["concrete"]["dry_volume"] * self.data["concrete"]["wet_volume_constant"] 

    def __repr__(self) -> str:
        import json
        return json.dumps(self.data)

# Tests
fdn = {
    "length": 90,
    "width": 0.457,
    "depth": 1.22,
    "thickness": 0.35,
    "mb_type": "m16",
    "mb_amt": 3,
    "lnk_type": "m10",
    "lnk_spaceing": 0.2 
}

 

from tkinter import *
from tkinter import ttk
root = Tk()
#Define the geometry of the window
root.geometry("550x250")
s=ttk.Style()
s.theme_use('clam')
# Add the rowheight
#s.configure('Label', rowheight=40)
s.configure('Row', rowheight=40)

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Length").grid(column=0, row=0)
ttk.Label(frm, text="Width").grid(column=0, row=1)
ttk.Label(frm, text="Depth").grid(column=0, row=2)
ttk.Label(frm, text="Thickness").grid(column=0, row=3)


e1 = ttk.Entry(frm)
e2 = ttk.Entry(frm)
e3 = ttk.Entry(frm)
e4 = ttk.Entry(frm)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

e3.grid(row=2, column=1)

e4.grid(row=3, column=1)

def process_data():
    fdn['length'] = float(e1.get())
    fdn['width'] = float(e2.get())
    fdn['depth'] = float(e3.get())
    fdn['thickness'] = float(e4.get())
    
    strip_fdn = StripFoundation(fdn)
    strip_fdn.set_volume()
    exc = strip_fdn.data.get('excavation')
    conc = strip_fdn.data.get('concrete') 
    msg = ttk.Label(frm, text=f"Excavation: {round(exc.get('value'),3)} {exc.get('unit')}").grid(column=3, row=0)
    msg1 = ttk.Label(frm, text= f"Concrete: Dry {round(conc.get('dry_volume'),3)} {conc.get('unit')} | Wet {round(conc.get('wet_volume'),3)} {conc.get('unit')}").grid(column=3, row=1)
    msg.config(font=('times', 8, 'italic'))
    
    
    print(strip_fdn)

ttk.Button(frm, text="Process", command=process_data).grid(column=0, row=5)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=5)


root.mainloop()
