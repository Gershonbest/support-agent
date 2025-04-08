def store_procedural_memory(skill_name, steps):
    session = SessionLocal()
    existing = session.query(ProceduralMemory).filter_by(skill_name=skill_name).first()
    if existing:
        existing.steps = steps
    else:
        session.add(ProceduralMemory(skill_name=skill_name, steps=steps))
    session.commit()
    session.close()

def retrieve_procedural_memory(skill_name):
    session = SessionLocal()
    result = session.query(ProceduralMemory).filter_by(skill_name=skill_name).first()
    session.close()
    return result.steps if result else "No procedural memory found."
