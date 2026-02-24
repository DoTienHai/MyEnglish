"""Paragraph fixtures - Sample data for testing"""
import pytest


@pytest.fixture
def sample_paragraph_base() -> dict:
    """Base paragraph data for testing - 50% completed"""
    return {
        "id": None,
        "title": "Test Translation Session",
        "input_paragraph": """The quick brown fox jumps over the lazy dog. This is a common English sentence used to test various typewriters and computer keyboards. It contains every letter of the English alphabet at least once. The sentence is famous because of its unique property. It is often used in practice exercises and typing tests. Many people find it useful for learning keyboard layouts.""",
        "reference": "English Typing Tutorial",
        "machine_translation": """Con cáo nâu nhanh nhảy qua con chó lười biếng. Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra các máy chữ khác nhau và bàn phím máy tính. Nó chứa mỗi chữ cái của bảng chữ cái tiếng Anh ít nhất một lần. Câu này nổi tiếng vì tính chất độc đáo của nó. Nó thường được sử dụng trong các bài tập luyện tập và bài kiểm tra gõ phím. Nhiều người thấy nó hữu ích để học bố cục bàn phím.""",
        "completed": 50.0,
        "score": 8.5,
        "created_at": "2026-01-26 12:00:00"
    }


@pytest.fixture
def paragraph_factory(sample_paragraph_base: dict):
    """Factory for creating paragraph dicts with overrides"""
    def _factory(**overrides):
        data = dict(sample_paragraph_base)
        data.update(overrides)
        return data

    return _factory


@pytest.fixture
def sample_paragraph_completed() -> dict:
    """Completed paragraph data - 100% completed"""
    return {
        "id": None,
        "title": "Completed Session",
        "input_paragraph": """Learning English is a rewarding journey that opens many doors. When you commit to studying consistently, you will notice improvements in your vocabulary, grammar, and pronunciation. Many students find that reading books, watching movies, and practicing conversations are the most effective ways to learn. Dedication and practice are the keys to success. With time and effort, you will become fluent and confident in using English.""",
        "reference": "English Learning Guide",
        "machine_translation": """Học tiếng Anh là một hành trình bổ ích mở ra nhiều cơ hội. Khi bạn cam kết học tập một cách liên tục, bạn sẽ thấy cải thiện trong từ vựng, ngữ pháp và cách phát âm. Nhiều học sinh thấy rằng đọc sách, xem phim và luyện tập hội thoại là những cách hiệu quả nhất để học. Sự tận tâm và luyện tập là chìa khóa thành công. Với thời gian và nỗ lực, bạn sẽ trở nên lưu loát và tự tin khi sử dụng tiếng Anh.""",
        "completed": 100.0,
        "score": 9.5,
        "created_at": "2026-01-25 10:00:00"
    }


@pytest.fixture
def sample_paragraph_incomplete() -> dict:
    """In-progress paragraph data - 75% completed"""
    return {
        "id": None,
        "title": "In Progress Session",
        "input_paragraph": """Practice makes perfect. This is an old saying that has been proven true by countless learners worldwide. The more you engage with a language, the better you become at it. Every mistake is a step forward in your learning journey. You should practice daily, even if only for a few minutes. Consistency is more important than intensity when it comes to language acquisition.""",
        "reference": "Motivational Learning Quote",
        "machine_translation": """Luyện tập làm nên sẽ hoàn hảo. Đây là một câu nói cũ đã được chứng minh là đúng bởi vô số người học trên toàn thế giới. Bạn tiếp xúc với ngôn ngữ càng nhiều, bạn càng trở nên giỏi hơn. Mỗi sai lầm là một bước tiến trong hành trình học tập của bạn. Bạn nên luyện tập hàng ngày, ngay cả khi chỉ trong vài phút. Tính nhất quán quan trọng hơn cường độ khi nói đến việc tiếp thu ngôn ngữ.""",
        "completed": 75.0,
        "score": 8.0,
        "created_at": "2026-01-24 14:30:00"
    }


@pytest.fixture
def sample_paragraph_open() -> dict:
    """Open (not started) paragraph data - 0% completed"""
    return {
        "id": None,
        "title": "Not Started Session",
        "input_paragraph": """Start learning today and invest in your future. English is the global language of business, science, and communication. By learning English, you open doors to countless opportunities around the world. Whether you are learning for work, travel, or personal enrichment, you are making a valuable investment in yourself. Do not wait for the perfect moment; the best time to start is now. Begin your English learning journey today with determination and enthusiasm.""",
        "reference": "English Learning Motivation",
        "machine_translation": """Bắt đầu học hôm nay và đầu tư cho tương lai của bạn. Tiếng Anh là ngôn ngữ toàn cầu của kinh doanh, khoa học và giao tiếp. Bằng cách học tiếng Anh, bạn mở cửa cho vô số cơ hội trên toàn thế giới. Dù bạn đang học vì công việc, du lịch hay làm giàu cá nhân, bạn đang đầu tư giá trị cho chính mình. Đừng chờ đợi khoảnh khắc hoàn hảo; thời gian tốt nhất để bắt đầu là bây giờ. Bắt đầu hành trình học tiếng Anh của bạn ngay hôm nay với sự quyết tâm và nhiệt huyết.""",
        "completed": 0.0,
        "score": 0.0,
        "created_at": "2026-01-23 09:00:00"
    }


# ============ Builder Fixtures (tạo model objects từ dicts) ============

@pytest.fixture
def sample_paragraph_base_model(sample_paragraph_base: dict):
    """Paragraph model - 50% completed"""
    from model.paragraph import Paragraph
    return Paragraph(**sample_paragraph_base)


@pytest.fixture
def sample_paragraph_completed_model(sample_paragraph_completed: dict):
    """Paragraph model - 100% completed"""
    from model.paragraph import Paragraph
    return Paragraph(**sample_paragraph_completed)


@pytest.fixture
def sample_paragraph_incomplete_model(sample_paragraph_incomplete: dict):
    """Paragraph model - 75% completed"""
    from model.paragraph import Paragraph
    return Paragraph(**sample_paragraph_incomplete)


@pytest.fixture
def sample_paragraph_open_model(sample_paragraph_open: dict):
    """Paragraph model - 0% completed"""
    from model.paragraph import Paragraph
    return Paragraph(**sample_paragraph_open)


