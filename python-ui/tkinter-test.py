from tkinter import Tk
import tkinter as tkel
import tkinter.ttk as ttk
import random

class Receiver(object):
  def __init__(self):
    self.subscriptions = {}
  def subscribe(self, msg, callback):
    if msg in self.subscriptions:
      self.subscriptions[msg].append(callback)
    else:
      self.subscriptions[msg] = [callback]
  def on_msg(self, msg, data):
    if msg in self.subscriptions:
      for cb in self.subscriptions[msg]:
        cb(data)

def send(msg):
  print("SEND " + msg)
  if msg == "ping":
    global ctx
    ctx.rec.on_msg("ping", random.randint(0, 9999))
  if msg == "v1:off":
    ctx.rec.on_msg("fm1", 0)
  elif msg == "v1:on":
    ctx.rec.on_msg("fm1", 100)
    
def sender(msg):
  return lambda: send(msg)

class Ctx(object):
  def __init__(self, frm, rec):
    self.frm = frm
    self.rec = rec
class Element(object):
  def __init__(self, el):
    self.el = el
class Toggle(Element):
  def __init__(self, ctx, label, istate=False, on_state_change=lambda _old, _new : ()):
    Element.__init__(self, tkel.Button(ctx.frm, text=label, command=self.toggle))
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
  def __init__(self, ctx, label, on_click=lambda : ()):
    Element.__init__(self, tkel.Button(ctx.frm, text=label, command=on_click))
class SenderToggle(Toggle):
  def __init__(self, ctx, label, istate=False):
    Toggle.__init__(self, ctx, label, istate, on_state_change= (lambda _old, new : send(f"{label}:" + ("on" if new else "off"))))
class Display(Element):
  def __init__(self, ctx, msg, fmt=lambda data : str(data), idata="[no data]"):
    Element.__init__(self, tkel.Label(ctx.frm, text=fmt(idata)))
    ctx.rec.subscribe(msg, lambda data : self.el.config(text=fmt(data)))
class LabelDisplay(Display):
  def __init__(self, ctx, msg, label, idata="[no data]"):
    Display.__init__(self, ctx, msg, fmt=lambda data : f"{label}: {data}", idata=idata)
    
root = Tk()

frm = ttk.Frame(root)
frm.config(padding=10)
frm.grid()

ctx = Ctx(frm, Receiver())

btns = [
    [SenderToggle(ctx, "v1"), SenderToggle(ctx, "v2"), SenderToggle(ctx, "v3")],
    [Button(ctx, "abort", sender("abort")), Button(ctx, "ping", sender("ping"))],
    [LabelDisplay(ctx, "ping", "ping"), LabelDisplay(ctx, "fm1", "Flow")]
]

tkel.Label(frm, text="Valve control").grid(column=0, row=0)

for coli, row in enumerate(btns):
  for rowi, btn in enumerate(row):
    btn.el.grid(column=coli, row=1 + rowi)
    #tkel.Button(frm, text=msg, command=sender(msg)).grid(column=coli, row=1 + rowi)

root.mainloop()