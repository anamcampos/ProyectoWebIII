from sqlalchemy import (create_engine, Column, Integer, String, Text,
                        DateTime, JSON, ForeignKey, func)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), index=True)
    file_name = Column(String)
    file_path = Column(Text)
    sha256 = Column(String)
    version = Column(Integer, default=1)
    last_checked = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relación opcional
    item = relationship("Item", backref="files")

    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "sha256": self.sha256,
            "version": self.version,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None
        }


def get_files_by_item(session, item_id):
    return session.query(File).filter_by(item_id=item_id).all()

def find_file_by_name(session, item_id, file_name):
    return session.query(File).filter_by(item_id=item_id, file_name=file_name).one_or_none()

def upsert_file_record(session, item_id, file_name, file_path, sha256_val):
    """
    Inserta o actualiza un registro de archivo para un item.
    Si existe y sha diff => incrementa version y actualiza sha + path.
    """
    f = find_file_by_name(session, item_id, file_name)
    if f is None:
        f = File(item_id=item_id, file_name=file_name, file_path=file_path, sha256=sha256_val, version=1)
        session.add(f)
        session.flush()
        return {"action": "created", "file": f.to_dict()}
    else:
        if f.sha256 != sha256_val:
            old_version = f.version
            f.version = (f.version or 1) + 1
            f.sha256 = sha256_val
            f.file_path = file_path
            session.flush()
            return {"action": "replaced", "old_version": old_version, "file": f.to_dict()}
        else:
            session.flush()
            return {"action": "unchanged", "file": f.to_dict()}

def delete_file_record(session, file_record):
    """
    Elimina registro de File (no borra el archivo local — hacerlo desde main)
    """
    session.delete(file_record)
    session.flush()
