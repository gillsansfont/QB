import os, io
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from scipy.signal import convolve2d
from quantumblur.quantumblur import QuantumBlur

# (Optional) Qiskit Runtime setup…
if os.environ.get("JyFqdslIKjEPocpvFvm_9DxqdsSyV5giahkHH06u_dkr"):
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=os.environ["JyFqdslIKjEPocpvFvm_9DxqdsSyV5giahkHH06u_dkr"]
    )
    qb = QuantumBlur(size=99, rotations=3, shots=2048, backend=service)
else:
    qb = QuantumBlur(size=99, rotations=3, shots=2048)

# ——— Here’s the CORS Setup ———
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or lock down to your Hydra domain
    allow_methods=["*"],        # GET, POST, etc.
    allow_headers=["*"],        # Content-Type, Authorization, …
    allow_credentials=True,     # if you ever need cookies/auth
)
# ————————————————————————

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        frame = await ws.receive_bytes()
        img   = Image.open(io.BytesIO(frame)).convert("L")
        arr   = np.array(img)

        kernel  = qb.get_kernel()
        blurred = convolve2d(arr, kernel, mode="same", boundary="wrap")
        out     = Image.fromarray(np.clip(blurred,0,255).astype(np.uint8))

        buf = io.BytesIO()
        out.save(buf, format="JPEG", quality=80)
        await ws.send_bytes(buf.getvalue())
