# taste_profile.py - 간소화 버전
class TasteProfile:
    """위스키의 맛 프로필을 나타내는 클래스"""
    
    def __init__(self, sweetness=0, smoky=0, fruity=0, spicy=0):
        """맛 프로필 초기화"""
        self.sweetness = sweetness  # 단맛 (0-5)
        self.smoky = smoky          # 스모키함 (0-5)
        self.fruity = fruity        # 과일향 (0-5)
        self.spicy = spicy          # 스파이시함 (0-5)
    
    def get_vector(self):
        """맛 프로필을 리스트로 반환"""
        return [self.sweetness, self.smoky, self.fruity, self.spicy]
    
    def __str__(self):
        """문자열 표현"""
        return f"단맛: {self.sweetness}, 스모키: {self.smoky}, 과일향: {self.fruity}, 스파이시: {self.spicy}"