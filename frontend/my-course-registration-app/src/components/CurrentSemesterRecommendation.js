// src/components/CurrentSemesterRecommendation.js
import React from 'react'; // useState は使わないので削除
import { useNavigate } from 'react-router-dom';
import './CurrentSemesterRecommendation.css';

function CurrentSemesterRecommendation() {
  const navigate = useNavigate();

  // 以前の、詳細な情報を含むダミーデータ
  const dummyRecommendation = {
    totalUnitsOverall: 124, // 卒業までの総単位数
    remainingUnitsOverall: 12, // 卒業までの残単位数
    itSkillAcquisitionRate: 88, // 基本情報技術者試験内容習得率

    currentSemester: {
      year: 2025,
      semester: '前期',
      totalUnits: 15,
      requiredUnits: 8,
      electiveUnits: 7,
    },
    recommendedCourses: [
      { code: 'CS101', name: '情報科学概論', units: 2, type: '必修', description: 'コンピュータの基礎を学ぶ' },
      { code: 'MA201', name: '線形代数II', units: 2, type: '必修', description: '数学的思考力を養う' },
      { code: 'PR301', name: 'オブジェクト指向プログラミング', units: 3, type: '選択', description: '実践的なプログラミングスキル' },
      { code: 'SE401', name: 'ソフトウェア工学', units: 3, type: '選択', description: '効率的なソフトウェア開発手法' },
      { code: 'EL105', name: '英語コミュニケーションI', units: 2, type: '選択', description: '英語でのコミュニケーション能力' },
      { code: 'PH101', name: '基礎物理学', units: 3, type: '教養', description: '物理学の基礎概念' },
    ],
    notes: 'この今学期の履修計画は、あなたの希望条件（例：AI分野興味、週3日登校希望）に基づいています。',
    advice: '情報技術者試験の合格を目指す場合、夏期休暇中に専門書を読むことをお勧めします。',
  };

  const {
    totalUnitsOverall,
    remainingUnitsOverall,
    itSkillAcquisitionRate,
    currentSemester,
    recommendedCourses,
    notes,
    advice
  } = dummyRecommendation;

  // 「次へ」ボタンでW7へ遷移
  const handleGoToFourYearPattern = () => {
    console.log('4年間の履修パターン候補（W7）へ遷移');
    navigate('/patterns'); // W7のパス
  };

  // 「条件に戻る」ボタン（代替フローなど）
  const handleGoBackToConditions = () => {
    console.log('希望条件の入力ページ（W6）へ戻る');
    alert('希望条件の入力ページ（W6）へ戻ります。');
    // navigate('/conditions'); // 仮にW6のパスが /conditions の場合
  };

  return (
    <div className="recommendation-container">
      <h2>今学期のおすすめ履修登録</h2>

      <div className="summary-section">
        <h3>全体概要</h3>
        <p><strong>卒業までの総単位数:</strong> {totalUnitsOverall}単位</p>
        <p><strong>卒業までの残単位数:</strong> {remainingUnitsOverall}単位</p>
        <p><strong>基本情報技術者試験内容習得率:</strong> {itSkillAcquisitionRate}%</p>
      </div>

      <div className="semester-summary-section">
        <h3>今学期の履修概要（{currentSemester.year}年 {currentSemester.semester}）</h3>
        <p><strong>今学期総単位数:</strong> {currentSemester.totalUnits}単位</p> {/* プロパティ名を修正 */}
        <p><strong>必修単位数:</strong> {currentSemester.requiredUnits}単位</p> {/* プロパティ名を修正 */}
        <p><strong>選択単位数:</strong> {currentSemester.electiveUnits}単位</p> {/* プロパティ名を修正 */}
      </div>

      <div className="courses-section">
        <h3>おすすめ科目一覧</h3>
        <table>
          <thead>
            <tr>
              <th>科目コード</th>
              <th>科目名</th>
              <th>単位</th>
              <th>種別</th>
              <th>概要</th>
            </tr>
          </thead>
          <tbody>
            {recommendedCourses.map((course, index) => (
              <tr key={index}>
                <td>{course.code}</td>
                <td>{course.name}</td>
                <td>{course.units}</td>
                <td>{course.type}</td>
                <td>{course.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {notes && (
        <div className="notes-section">
          <h3>特記事項</h3>
          <p>{notes}</p>
        </div>
      )}

      {advice && (
        <div className="advice-section">
          <h3>アドバイス</h3>
          <p>{advice}</p>
        </div>
      )}

      <div className="action-buttons">
        <button onClick={handleGoBackToConditions} className="back-button">
          希望条件のページに戻る
        </button>
        <button onClick={handleGoToFourYearPattern} className="next-button">
          次へ（4年間の履修パターンを見る）
        </button>
      </div>
    </div>
  );
}

export default CurrentSemesterRecommendation;