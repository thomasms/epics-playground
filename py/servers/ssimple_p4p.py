from p4p.nt import NTScalar
from p4p.server import Server
from p4p.server.thread import SharedPV

pv1 = SharedPV(nt=NTScalar('d'),
              initial=0.0)
pv2 = SharedPV(nt=NTScalar('d'),
              initial=4.2)
pv3 = SharedPV(nt=NTScalar('d'),
              initial=24.2346692)

@pv1.put
@pv2.put
@pv3.put
def handleput(pv, op):
    print(f"You changed my value to: {op.value().raw['value']}, I used to be: {pv.current().raw['value']}")
    pv.post(op.value())
    op.done()

Server.forever(providers=[
    {
        'p4p:pv1':pv1,
        'p4p:pv2':pv2,
        'p4p:pv3':pv3,
    }
])

