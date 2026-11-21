 
 
def get_regions(ref, uem):
    """Таймлайны single (1 спикер), overlap (>=2), nonspeech внутри UEM."""
    ref = ref.support()
    speech = ref.get_timeline().support()
    overlap = ref.get_overlap()
    single = speech.extrude(overlap)
    nonspeech = uem.extrude(speech)
    crop = lambda tl: tl.crop(uem, mode="intersection")
    return {"single": crop(single), "overlap": crop(overlap), "nonspeech": crop(nonspeech)}
 