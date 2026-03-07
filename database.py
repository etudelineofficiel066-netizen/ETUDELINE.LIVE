from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base
import os

EXTERNAL_DB_URL = os.getenv("EXTERNAL_DATABASE_URL") or os.getenv("RENDER_DATABASE_URL")
REPLIT_DB_URL = os.getenv("DATABASE_URL")
IS_RENDER = os.getenv("RENDER") == "true"

if EXTERNAL_DB_URL:
    DATABASE_URL = EXTERNAL_DB_URL
    print("=" * 70)
    print("🔵 CONNEXION À LA BASE DE DONNÉES EXTERNE (RENDER POSTGRESQL)")
    host = DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'
    print(f"   Host: {host}")
    print("   ⚠️  ATTENTION : Vos données sont sur cette base - NE PAS LA SUPPRIMER")
    print("=" * 70)
elif REPLIT_DB_URL:
    DATABASE_URL = REPLIT_DB_URL
    print("=" * 70)
    print("⚠️  CONNEXION À LA BASE DE DONNÉES REPLIT (LOCALE)")
    print("   PROBLÈME : Cette base n'est PAS persistante sur Render !")
    print("   SOLUTION : Configurez EXTERNAL_DATABASE_URL sur Render")
    print("=" * 70)
else:
    DATABASE_URL = None
    print("=" * 70)
    print("❌ AUCUNE BASE DE DONNÉES CONFIGURÉE !")
    print("   Sur Render : ajoutez EXTERNAL_DATABASE_URL dans les variables d'environnement")
    print("=" * 70)


def _build_engine(url: str):
    """Construire l'engine SQLAlchemy avec les bons paramètres selon l'URL."""
    if not url:
        raise RuntimeError(
            "DATABASE_URL non configurée. "
            "Sur Render, définissez EXTERNAL_DATABASE_URL dans les variables d'environnement."
        )

    # Si sslmode est déjà dans l'URL, ne pas le repasser dans connect_args (évite les conflits)
    has_ssl_in_url = "sslmode=" in url

    engine_kwargs = dict(
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
        pool_recycle=300,
    )

    if not has_ssl_in_url:
        ssl_mode = "require" if IS_RENDER else "prefer"
        engine_kwargs["connect_args"] = {"sslmode": ssl_mode}

    return create_engine(url, **engine_kwargs)


engine = _build_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Créer toutes les tables"""
    Base.metadata.create_all(bind=engine)


def reset_database():
    """Supprimer et recréer toutes les tables"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def check_db_connection() -> bool:
    """Vérifie que la connexion à la base de données fonctionne."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Test connexion BD échoué : {e}")
        return False
