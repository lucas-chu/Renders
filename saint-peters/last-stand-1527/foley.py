"""Deterministic, original contact and footstep sounds mixed quietly beneath Ave Maria."""
import numpy as np, wave
def make(path):
 R=48000;rng=np.random.default_rng(1527);a=np.zeros((R*30,2))
 def note(start,kind,vol,pan):
  n=int(.72*R);t=np.arange(n)/R
  if kind=='steel':
   y=sum(np.sin(2*np.pi*(f*rng.uniform(.97,1.03))*t)*amp*np.exp(-t/decay) for f,amp,decay in [(1160,.44,.12),(1691,.22,.21),(2784,.18,.075),(3718,.11,.18)])
   y+=rng.normal(0,.24,n)*np.exp(-t/.012)
  else:
   y=np.sin(2*np.pi*(56*t+1.9*(1-np.exp(-t/.025))))*.46*np.exp(-t/.071)
   noise=rng.normal(0,1,n);y+=np.convolve(noise,np.ones(19)/19,mode='same')*.72*np.exp(-t/.05)
  y*=np.minimum(t/.002,1)*vol
  p=int(R*start)
  a[p:p+n]+=y[:,None]*np.array([np.sqrt(1-pan),np.sqrt(pan)])
  if 16<start<24:a[p+2342:p+n+2342]+=y[:,None]*.15
 for t in np.arange(2.1,15.6,.46):note(t+rng.uniform(-.085,.085),'foot',rng.uniform(.025,.071),rng.uniform(.15,.85))
 for t in [8.5,9.43,10.65,11.1,11.8,12.77,13.35,14.31,15.22,24.38,25.18]:note(t,'steel',rng.uniform(.047,.092),rng.uniform(.13,.87))
 for t in np.arange(16.24,23.87,.44):note(t,'foot',rng.uniform(.044,.068),rng.uniform(.20,.8))
 with wave.open(str(path),'wb') as w:w.setparams((2,2,R,0,'NONE','not compressed'));w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
