from tkinter import Tk
import tkinter as tkel
import tkinter.ttk as ttk

def send(msg):
  print("SEND " + msg)
def sender(msg):
  return lambda: send(msg)

class Element(object):
  def __init__(self, el):
    self.el = el
class Toggle(Element):
  def __init__(self, frm, label, istate=False, on_state_change=lambda _old, _new : ()):
    Element.__init__(self, tkel.Button(frm, text=label, command=self.toggle))
    self.on_state_change = on_state_change
    self._state = None
    self.state = istate
  @property
  def state(self):
    return self._state
  @state.setter
  def state(self, state):
    if self._state is not None:
      if state != self._state:
        self.on_state_change(self._state, state)
    self._state = state
    self.el.config(foreground = "red" if state else "blue")
  def toggle(self):
    self.state = not self.state
class Button(Element):
  def __init__(self, frm, label, on_click=lambda : ()):
    Element.__init__(self, tkel.Button(frm, text=label, command=on_click))
class SenderToggle(Toggle):
  def __init__(self, frm, label, istate=False):
    Toggle.__init__(self, frm, label, istate, on_state_change= (lambda _old, new : send(f"{label}:" + ("on" if new else "off"))))
    

root = Tk()

frm = ttk.Frame(root)
frm.config(padding=10)
frm.grid()

btns = [
    [SenderToggle(frm, "v1"), SenderToggle(frm, "v2"), SenderToggle(frm, "v3")],
    [Button(frm, "abort", sender("abort")), Button(frm, "ping", sender("ping"))]
]

tkel.Label(frm, text="Valve control").grid(column=0, row=0)

for coli, row in enumerate(btns):
  for rowi, btn in enumerate(row):
    btn.el.grid(column=coli, row=1 + rowi)
    #tkel.Button(frm, text=msg, command=sender(msg)).grid(column=coli, row=1 + rowi)

root.mainloop()