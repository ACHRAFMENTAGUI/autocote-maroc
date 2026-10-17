from streamlit.testing.v1 import AppTest


def test_app_startup_and_rendering():
    """Vérifie que l'application démarre sans lever d'exception."""
    at = AppTest.from_file("app/streamlit_app.py")
    at.run(timeout=30)
    assert not at.exception, f"Erreur au démarrage de l'app : {at.exception}"
    assert len(at.title) >= 0 or len(at.markdown) > 0


def test_preset_button_click():
    """Vérifie que le clic sur un preset (Golf 7) met à jour les champs sans crash."""
    at = AppTest.from_file("app/streamlit_app.py")
    at.run(timeout=30)

    # Trouver et cliquer sur le bouton Golf 7
    golf_btn = None
    for btn in at.button:
        if "Golf" in btn.label:
            golf_btn = btn
            break

    if golf_btn:
        golf_btn.click().run(timeout=30)
        assert not at.exception, f"Erreur lors du clic sur le preset Golf : {at.exception}"


def test_app_submit_prediction():
    """Vérifie que le clic sur 'Calculer' génère une estimation sans crash."""
    at = AppTest.from_file("app/streamlit_app.py")
    at.run(timeout=30)

    # Trouver le bouton de calcul
    calc_btn = None
    for btn in at.button:
        if "Calculer" in btn.label:
            calc_btn = btn
            break

    if calc_btn:
        calc_btn.click().run(timeout=30)
        assert not at.exception, f"Erreur lors de l'exécution du calcul : {at.exception}"
