
import streamlit as st
import json
import re
from datetime import datetime

st.set_page_config(
    page_title="Tick Tock Studio",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #100f24, #211536);
    color: white;
}
h1, h2, h3, p, label { color: white !important; }
.stButton button {
    background: linear-gradient(90deg,#895cff,#e879c9);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 TICK TOCK STUDIO")
st.caption("Your All-in-One AI Video Creator")

st.sidebar.title("🎥 Select Channel")
channel = st.sidebar.selectbox(
    "Your YouTube Channel",
    ["Mini Masti Pop", "Tiny Tadka", "Zariya Style"]
)

settings = {
    "Mini Masti Pop": {
        "duration": ["1 minute", "2 minutes", "3 minutes", "5 minutes", "7 minutes"],
        "style": "2D hand-drawn cinematic horror animation"
    },
    "Tiny Tadka": {
        "duration": ["1 minute"],
        "style": "Ultra-realistic miniature ASMR food cinematography"
    },
    "Zariya Style": {
        "duration": ["1 minute"],
        "style": "High-quality Indian fashion showcase"
    }
}

st.sidebar.success(f"Selected: {channel}")
st.sidebar.info("Daily target: 3 videos")

st.header("✨ Create Your Video")

duration = st.selectbox(
    "Video Duration",
    settings[channel]["duration"]
)

if channel == "Mini Masti Pop":
    aspect = st.selectbox("Video Format", ["16:9 Long Video", "9:16 Shorts"])
    scene_seconds = 12
elif channel == "Tiny Tadka":
    aspect = "9:16 Shorts"
    scene_seconds = 10
else:
    aspect = "9:16 Shorts"
    scene_seconds = 10

story = st.text_area(
    "Enter your story or video idea",
    placeholder="Yahan apni kahani ya video ka idea likho...",
    height=150
)

def get_seconds(value):
    number = int(value.split()[0])
    return number * 60

def make_scenes(idea, total_seconds, scene_seconds, style, channel):
    count = (total_seconds + scene_seconds - 1) // scene_seconds
    scenes = []

    horror_beats = [
        "Establish the location, atmosphere and mysterious surroundings.",
        "Introduce the main character and the unusual situation.",
        "Show the first strange event and build suspense.",
        "Reveal a clue that changes the character's understanding.",
        "Increase tension with a surprising discovery.",
        "Show the main twist and the character's reaction.",
        "Build toward the climax with cinematic suspense.",
        "Deliver the climax and a memorable ending."
    ]

    for i in range(count):
        beat = horror_beats[i % len(horror_beats)]
        if channel == "Mini Masti Pop":
            action = beat
            sound = "Creepy ambient drone, wind and subtle suspense effects."
            voice = "Hindi horror narration, expressive and suspenseful."
        elif channel == "Tiny Tadka":
            action = [
                "Show miniature chefs preparing fresh ingredients.",
                "Show precise cutting and preparation with tiny utensils.",
                "Show ingredients cooking in a miniature pan.",
                "Show spices and sauces being added in close-up.",
                "Show realistic sizzling and stirring.",
                "Show the final cooking steps and plating."
            ][i % 6]
            sound = "Realistic cooking ASMR, sizzling, chopping and utensil sounds."
            voice = "No dialogue. Pure miniature cooking ASMR."
        else:
            action = [
                "Introduce the outfit with a stylish full-body shot.",
                "Show the fabric, texture and fine details.",
                "Show the neckline, sleeves and embroidery.",
                "Show the dupatta and outfit styling.",
                "Show elegant walking and natural fabric movement.",
                "Finish with a beautiful complete outfit showcase."
            ][i % 6]
            sound = "Soft fashionable background music."
            voice = "Optional short Hindi fashion narration."

        prompt = f"""
SCENE {i+1}
Duration: {min(scene_seconds, total_seconds-i*scene_seconds)} seconds

VIDEO IDEA:
{idea}

SCENE ACTION:
{action}

VISUAL STYLE:
{style}

CHARACTER AND VISUAL CONSISTENCY:
Keep the same characters, faces, clothes, colours and locations
consistent throughout the entire video.

CAMERA:
Cinematic composition, smooth camera movement,
clear subject and detailed background.

VOICE:
{voice}

SOUND:
{sound}

FORMAT:
{aspect}
"""
        scenes.append({
            "number": i+1,
            "duration": min(scene_seconds, total_seconds-i*scene_seconds),
            "prompt": prompt.strip()
        })

    return scenes

if st.button("🚀 GENERATE VIDEO PLAN", use_container_width=True):
    if not story.strip():
        st.error("Please enter a story or video idea first.")
    else:
        total = get_seconds(duration)
        style = settings[channel]["style"]
        scenes = make_scenes(story, total, scene_seconds, style, channel)

        st.session_state["scenes"] = scenes
        st.session_state["channel"] = channel
        st.session_state["idea"] = story
        st.session_state["duration"] = duration

if "scenes" in st.session_state:
    scenes = st.session_state["scenes"]

    st.success(
        f"Plan ready! {len(scenes)} scenes | "
        f"{st.session_state['duration']} | "
        f"{st.session_state['channel']}"
    )

    for scene in scenes:
        with st.expander(
            f"Scene {scene['number']} — {scene['duration']} seconds"
        ):
            st.text_area(
                "Editable video prompt",
                scene["prompt"],
                height=230,
                key=f"scene_{scene['number']}"
            )

    export_data = {
        "channel": st.session_state["channel"],
        "idea": st.session_state["idea"],
        "duration": st.session_state["duration"],
        "scenes": [
            {
                "number": s["number"],
                "duration": s["duration"],
                "prompt": st.session_state.get(
                    f"scene_{s['number']}", s["prompt"]
                )
            }
            for s in scenes
        ]
    }

    st.download_button(
        "📥 Download All Scene Prompts (JSON)",
        json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name="tick_tock_video_plan.json",
        mime="application/json",
        use_container_width=True
    )

    all_prompts = "\n\n".join(
        st.session_state.get(f"scene_{s['number']}", s["prompt"])
        for s in scenes
    )

    st.download_button(
        "📄 Download All Prompts (TXT)",
        all_prompts,
        file_name="tick_tock_prompts.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.caption(
    "TICK TOCK STUDIO | Version 1 | "
    "Video planning and prompt generation"
)
