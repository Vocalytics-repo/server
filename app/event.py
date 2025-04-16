# app/events.py
import numpy as np
import tempfile
import wave
from services.stt.stt_service import transcribe_with_whisper

audio_buffer = []

def register_sockets(sio):
    @sio.event
    async def connect(sid, environ):
        print(f"✅ 연결됨: {sid}")
        audio_buffer.clear()

    @sio.event
    async def audioData(sid, data):
        audio_buffer.append(np.frombuffer(data, dtype=np.int16))

    @sio.event
    async def endRecording(sid):
        audio = np.concatenate(audio_buffer)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            with wave.open(tmp.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio.tobytes())

            result = transcribe_with_whisper(tmp.name)
            await sio.emit("sttResult", {"text": result}, to=sid)
            audio_buffer.clear()