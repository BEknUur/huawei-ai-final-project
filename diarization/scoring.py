"""Оценка диаризации по регионам.
 
Правила: collar = 0, skip_overlap = False, один маппинг спикеров на митинг.
"""
 
 
def map_hypothesis(ref, hyp, uem):
    """Переименовать спикеров гипотезы по одному оптимальному маппингу на весь митинг."""
    raise NotImplementedError()
 
 
def score_meeting(ref, hyp, uem):
    """Секунды missed / false alarm / confusion / total для каждого региона."""
    raise NotImplementedError()
 