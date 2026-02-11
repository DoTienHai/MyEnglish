"""Model fixtures - Sample data for testing"""
import pytest
from model.paragraph import Paragraph
from model.sentence import Sentence
from model.vocabulary import Vocabulary


@pytest.fixture
def sample_paragraph() -> Paragraph:
    """Sample paragraph for testing"""
    return Paragraph(
        id=None,
        title="Test Translation Session",
        input_paragraph="""The quick brown fox jumps over the lazy dog. This is a common English sentence used to test various typewriters and computer keyboards. It contains every letter of the English alphabet at least once. The sentence is famous because of its unique property. It is often used in practice exercises and typing tests. Many people find it useful for learning keyboard layouts.""",
        reference="English Typing Tutorial",
        machine_translation="""Con cáo nâu nhanh nhảy qua con chó lười biếng. Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra các máy chữ khác nhau và bàn phím máy tính. Nó chứa mỗi chữ cái của bảng chữ cái tiếng Anh ít nhất một lần. Câu này nổi tiếng vì tính chất độc đáo của nó. Nó thường được sử dụng trong các bài tập luyện tập và bài kiểm tra gõ phím. Nhiều người thấy nó hữu ích để học bố cục bàn phím.""",
        completed=50.0,
        score=8.5,
        created_at="2026-01-26 12:00:00"
    )


@pytest.fixture
def sample_paragraph_completed() -> Paragraph:
    """Completed paragraph for testing"""
    return Paragraph(
        id=None,
        title="Completed Session",
        input_paragraph="""Learning English is a rewarding journey that opens many doors. When you commit to studying consistently, you will notice improvements in your vocabulary, grammar, and pronunciation. Many students find that reading books, watching movies, and practicing conversations are the most effective ways to learn. Dedication and practice are the keys to success. With time and effort, you will become fluent and confident in using English.""",
        reference="English Learning Guide",
        machine_translation="""Học tiếng Anh là một hành trình bổ ích mở ra nhiều cơ hội. Khi bạn cam kết học tập một cách liên tục, bạn sẽ thấy cải thiện trong từ vựng, ngữ pháp và cách phát âm. Nhiều học sinh thấy rằng đọc sách, xem phim và luyện tập hội thoại là những cách hiệu quả nhất để học. Sự tận tâm và luyện tập là chìa khóa thành công. Với thời gian và nỗ lực, bạn sẽ trở nên lưu loát và tự tin khi sử dụng tiếng Anh.""",
        completed=100.0,
        score=9.5,
        created_at="2026-01-25 10:00:00"
    )


@pytest.fixture
def sample_paragraph_incomplete() -> Paragraph:
    """In-progress paragraph for testing"""
    return Paragraph(
        id=None,
        title="In Progress Session",
        input_paragraph="""Practice makes perfect. This is an old saying that has been proven true by countless learners worldwide. The more you engage with a language, the better you become at it. Every mistake is a step forward in your learning journey. You should practice daily, even if only for a few minutes. Consistency is more important than intensity when it comes to language acquisition.""",
        reference="Motivational Learning Quote",
        machine_translation="""Luyện tập làm nên sẽ hoàn hảo. Đây là một câu nói cũ đã được chứng minh là đúng bởi vô số người học trên toàn thế giới. Bạn tiếp xúc với ngôn ngữ càng nhiều, bạn càng trở nên giỏi hơn. Mỗi sai lầm là một bước tiến trong hành trình học tập của bạn. Bạn nên luyện tập hàng ngày, ngay cả khi chỉ trong vài phút. Tính nhất quán quan trọng hơn cường độ khi nói đến việc tiếp thu ngôn ngữ.""",
        completed=75.0,
        score=8.0,
        created_at="2026-01-24 14:30:00"
    )


@pytest.fixture
def sample_paragraph_open() -> Paragraph:
    """Open (not started) paragraph for testing"""
    return Paragraph(
        id=None,
        title="Not Started Session",
        input_paragraph="""Start learning today and invest in your future. English is the global language of business, science, and communication. By learning English, you open doors to countless opportunities around the world. Whether you are learning for work, travel, or personal enrichment, you are making a valuable investment in yourself. Do not wait for the perfect moment; the best time to start is now. Begin your English learning journey today with determination and enthusiasm.""",
        reference="English Learning Motivation",
        machine_translation="""Bắt đầu học hôm nay và đầu tư cho tương lai của bạn. Tiếng Anh là ngôn ngữ toàn cầu của kinh doanh, khoa học và giao tiếp. Bằng cách học tiếng Anh, bạn mở cửa cho vô số cơ hội trên toàn thế giới. Dù bạn đang học vì công việc, du lịch hay làm giàu cá nhân, bạn đang đầu tư giá trị cho chính mình. Đừng chờ đợi khoảnh khắc hoàn hảo; thời gian tốt nhất để bắt đầu là bây giờ. Bắt đầu hành trình học tiếng Anh của bạn ngay hôm nay với sự quyết tâm và nhiệt huyết.""",
        completed=0.0,
        score=0.0,
        created_at="2026-01-23 09:00:00"
    )


@pytest.fixture
def sample_sentence() -> Sentence:
    """Sample sentence for testing"""
    return Sentence(
        id=None,
        paragraph_id=1,
        sentence_index=1,
        input_sentence="The quick brown fox jumps over the lazy dog.",
        user_translation="Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        machine_translation="Con cáo nâu nhanh nhảy qua con chó lười biếng.",
        score=0.95,
        note="Good translation",
        created_at="2026-01-26 12:00:00"
    )


@pytest.fixture
def sample_sentence_2() -> Sentence:
    """Sample sentence 2 for testing multiple sentences"""
    return Sentence(
        id=None,
        paragraph_id=1,
        sentence_index=2,
        input_sentence="This is a common English sentence used for testing.",
        user_translation="Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        machine_translation="Đây là một câu tiếng Anh phổ biến được sử dụng để kiểm tra.",
        score=0.88,
        note="Acceptable translation",
        created_at="2026-01-26 12:05:00"
    )


@pytest.fixture
def sample_vocabulary() -> Vocabulary:
    """Sample vocabulary for testing"""
    return Vocabulary(
        id=None,
        word="serendipity",
        part_of_speech="noun",
        vi_meaning="Tình cờ may mắn, sự gặp gỡ vui vẻ khó lường",
        eng_description="The occurrence of events by chance in a happy or beneficial way",
        example="Meeting her was pure serendipity.",
        note="Common word in English literature",
        correct_count=3,
        wrong_count=1,
        created_at="2026-01-26 12:00:00"
    )


@pytest.fixture
def sample_vocabulary_2() -> Vocabulary:
    """Sample vocabulary 2 for testing multiple vocabulary items"""
    return Vocabulary(
        id=None,
        word="ephemeral",
        part_of_speech="adjective",
        vi_meaning="Tạm thời, chỉ tồn tại trong thời gian ngắn",
        eng_description="Lasting for a very short time; transitory",
        example="The beauty of cherry blossoms is ephemeral.",
        note="Often used in poetry and literature",
        correct_count=2,
        wrong_count=0,
        created_at="2026-01-26 13:00:00"
    )
