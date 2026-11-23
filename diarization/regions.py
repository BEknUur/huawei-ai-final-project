def get_regions(ref, uem):
    """Timelines of single (1 speaker), overlap (>=2) and nonspeech regions inside the UEM."""
    ref = ref.support()
    speech = ref.get_timeline().support()
    overlap = ref.get_overlap()
    single = speech.extrude(overlap)
    nonspeech = uem.extrude(speech)
    return {
        "single": single.crop(uem, mode="intersection"),
        "overlap": overlap.crop(uem, mode="intersection"),
        "nonspeech": nonspeech.crop(uem, mode="intersection"),
    }
