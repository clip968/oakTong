class TasteProfile:
    # 맛 프로필 클래스
    
    def __init__(self, body=0, richness=0, smoke=0, sweetness=0):
        self.body = body  # 바디감 (0-5)
        self.richness = richness          # 깊이 (0-5)
        self.smoke = smoke        # 스모키 (0-5)
        self.sweetness = sweetness          # 단맛 (0-5)
    
    def get_vector(self):
        # 맛 프로필 벡터 반환
        return [self.body, self.richness, self.smoke, self.sweetness]
    
    # todo
    # 맛을 단맛, 스모키, 깊이, 무게감으로 바꿔야함
    def __str__(self):
        return f"바디감: {self.body}, 깊이: {self.richness}, 스모키: {self.smoke}, 단맛: {self.sweetness}"