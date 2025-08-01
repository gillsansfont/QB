import os, io
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from scipy.signal import convolve2d
from quantumblur.quantumblur import QuantumBlur

# Optional: if you want real-quantum hardware via Qiskit Runtime:
if os.environ.get("JyFqdslIKjEPocpvFvm_9DxqdsSyV5giahkHH06u_dkr"):
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService(channel="ibm_quantum", token=os.environ["JyFqdslIKjEPocpvFvm_9DxqdsSyV5giahkHH06u_dkr"])
    qb = QuantumBlur(size=99, rotations=3, shots=2048, backend=service)
else:
    qb = QuantumBlur(size=99, rotations=3, shots=2048)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # restrict in production!
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        frame = await ws.receive_bytes()            # incoming JPEG blob
        img = Image.open(io.BytesIO(frame)).convert("L")
        arr = np.array(img)

        # Generate new quantum‐blur kernel (or reuse if params static)
        kernel = qb.get_kernel()                    # from quantumblur.py :contentReference[oaicite:0]{index=0}

        # Convolve on the server
        blurred = convolve2d(arr, kernel, mode="same", boundary="wrap")
        out = Image.fromarray(np.clip(blurred, 0, 255).astype(np.uint8))

        buf = io.BytesIO()
        out.save(buf, format="JPEG", quality=80)
        await ws.send_bytes(buf.getvalue())
