// src/api.js

/**
 * API呼び出しをシミュレートするヘルパー関数
 * @param {any} data - 成功時に解決されるデータ
 * @param {number} delay - 遅延時間（ミリ秒）
 * @param {boolean} shouldFail - trueの場合、API呼び出しを失敗させる
 * @returns {Promise<any>}
 */
const simulateApiCall = (data, delay = 500, shouldFail = false) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error("API call failed (simulated)"));
      } else {
        resolve(data);
      }
    }, delay);
  });
};

// M12: 提案要求処理 (今学期のおすすめデータ) のモック
/**
 * 現在の学年に応じた今学期のおすすめ履修データを取得する。
 * @param {number} currentYear - 現在の学年 (例: 1, 2, 3, 4)
 * @returns {Promise<Object>} 今学期のおすすめデータ
 */
export const fetchCurrentSemesterRecommendation = async (currentYear = 1) => {
  console.log(`API: 今学期のおすすめデータ (学年: ${currentYear}) を取得中...`);

  let recommendedSubjects = [];
  let currentSemesterSchedule = {};
  let notes = '';

  switch (currentYear) {
    case 1:
      recommendedSubjects = [
        { id: 'math101', name: '応用数学I', units: 2, category: '専門科目', semester: '前期' },
        { id: 'prog203', name: 'オブジェクト指向プログラミング', units: 2, category: '専門科目', semester: '前期' },
        { id: 'net301', name: 'ネットワーク基礎', units: 2, category: '専門科目', semester: '前期' },
        { id: 'libarts05', name: '経済学原論', units: 2, category: '教養科目', semester: '前期' },
      ];
      currentSemesterSchedule = {
        '月': { '1限': '応用数学I', '2限': 'オブジェクト指向プログラミング', '3限': null, '4限': null, '5限': null },
        '火': { '1限': 'ネットワーク基礎', '2限': null, '3限': '経済学原論', '4限': null, '5限': null },
        '水': { '1限': null, '2限': '情報倫理', '3限': null, '4限': null, '5限': null },
        '木': { '1限': 'キャリアデザイン', '2限': null, '3限': null, '4限': null, '5限': null },
        '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
      };
      notes = '1年生向けのおすすめ科目です。基礎をしっかり固めましょう。';
      break;
    case 2:
      recommendedSubjects = [
        { id: 'ai201', name: '機械学習概論', units: 2, category: '専門科目', semester: '前期' },
        { id: 'db202', name: 'データベース設計', units: 2, category: '専門科目', semester: '前期' },
        { id: 'web203', name: 'Webアプリケーション開発', units: 2, category: '専門科目', semester: '前期' },
        { id: 'liberal204', name: '日本史', units: 2, category: '教養科目', semester: '前期' },
      ];
      currentSemesterSchedule = {
        '月': { '1限': '機械学習概論', '2限': 'データベース設計', '3限': null, '4限': null, '5限': null },
        '火': { '1限': 'Webアプリケーション開発', '2限': null, '3限': '日本史', '4限': null, '5限': null },
        '水': { '1限': null, '2限': 'OS基礎', '3限': null, '4限': null, '5限': null },
        '木': { '1限': '英語II', '2限': null, '3限': null, '4限': null, '5限': null },
        '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
      };
      notes = '2年生向けのおすすめ科目です。専門分野の基礎を深めましょう。';
      break;
    case 3:
      recommendedSubjects = [
        { id: 'cloud301', name: 'クラウドインフラ構築', units: 2, category: '専門科目', semester: '前期' },
        { id: 'sec302', name: '情報セキュリティ演習', units: 2, category: '専門科目', semester: '前期' },
        { id: 'proj303', name: 'プロジェクト管理', units: 2, category: '専門科目', semester: '前期' },
        { id: 'liberal304', name: '現代社会論', units: 2, category: '教養科目', semester: '前期' },
      ];
      currentSemesterSchedule = {
        '月': { '1限': 'クラウドインフラ構築', '2限': '情報セキュリティ演習', '3限': null, '4限': null, '5限': null },
        '火': { '1限': 'プロジェクト管理', '2限': null, '3限': '現代社会論', '4限': null, '5限': null },
        '水': { '1限': null, '2限': 'データサイエンス概論', '3限': null, '4限': null, '5限': null },
        '木': { '1限': 'ディベート', '2限': null, '3限': null, '4限': null, '5限': null },
        '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
      };
      notes = '3年生向けのおすすめ科目です。実践的なスキルを習得しましょう。';
      break;
    case 4:
      recommendedSubjects = [
        { id: 'grad_res', name: '卒業研究', units: 4, category: '専門科目', semester: '通年' },
        { id: 'internship', name: 'インターンシップ', units: 2, category: '専門科目', semester: '前期' },
        { id: 'seminar', name: '専門演習', units: 2, category: '専門科目', semester: '前期' },
        { id: 'career_dev', name: 'キャリア開発', units: 2, category: '教養科目', semester: '前期' },
      ];
      currentSemesterSchedule = {
        '月': { '1限': '卒業研究', '2限': 'インターンシップ', '3限': null, '4限': null, '5限': null },
        '火': { '1限': '専門演習', '2限': null, '3限': 'キャリア開発', '4限': null, '5限': null },
        '水': { '1限': null, '2限': '進路相談', '3限': null, '4限': null, '5限': null },
        '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
        '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
      };
      notes = '4年生向けのおすすめ科目です。卒業に向けて総仕上げを行いましょう。';
      break;
    default:
      // その他の学年の場合、デフォルトの1年生データを使用するか、エラーを返す
      recommendedSubjects = [];
      currentSemesterSchedule = {};
      notes = '該当する学年のおすすめ科目情報がありません。';
  }

  const dummyData = {
    totalUnits: 128, // 想定される卒業単位数
    remainingUnits: 16, // 残り単位数（これは学年によって変わるべきだが、今回は固定）
    basicTechExamCompletionRate: 85, // 基本情報技術者試験内容習得率 (%)（これも固定）
    recommendedSubjects,
    notes,
    currentSemesterSchedule,
    year: currentYear, // 受け取った学年をそのまま反映
    semester: '前期' // ここは固定とします。必要であれば引数に追加してください。
  };
  return simulateApiCall(dummyData);
};


// M12: 提案要求処理 (4年間の履修パターンデータ) のモック
/**
 * 4年間の履修パターンデータを取得する。
 * patternIdが指定された場合、そのIDのパターン詳細を返す。
 * 指定されない場合、全パターンの概要リストを返す。
 * @param {string|null} patternId - 取得したい履修パターンのID。全パターン取得の場合はnull。
 * @returns {Promise<Object|Array<Object>>} 履修パターンデータまたはそのリスト
 */
export const fetchFourYearPatterns = async (patternId = null) => {
  console.log(`API: 4年間の履修パターン (ID: ${patternId || '全パターン'}) データを取得中...`);

  // 時間割表形式のダミーデータ
  const fullDummyPatterns = [
    {
      id: 'pattern1',
      name: 'パターン1', // パターン名を通し番号に
      description: 'AI分野に重点を置いた標準的な履修パターン',
      totalUnits: 128,
      semesters: [
        {
          year: 1, semester: '前期',
          schedule: {
            '月': { '1限': '情報科学概論', '2限': 'プログラミング基礎', '3限': '英語コミュニケーションI', '4限': '基礎物理学', '5限': null },
            '火': { '1限': '線形代数I', '2限': 'プログラミング基礎', '3限': '情報科学概論', '4限': null, '5限': null },
            '水': { '1限': '英語コミュニケーションI', '2限': '基礎物理学', '3限': '線形代数I', '4限': null, '5限': null },
            '木': { '1限': '体育', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '社会学', '2限': '経済学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 1, semester: '後期',
          schedule: {
            '月': { '1限': 'データ構造とアルゴリズム', '2限': '人工知能入門', '3限': '微積分I', '4限': null, '5限': null },
            '火': { '1限': 'コンピュータ科学', '2限': '統計学', '3限': 'データ構造とアルゴリズム', '4限': null, '5限': null },
            '水': { '1限': '人工知能入門', '2限': '微積分I', '3限': 'プログラミング演習', '4限': null, '5限': null },
            '木': { '1限': '倫理学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '心理学', '2限': '応用数学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '前期',
          schedule: {
            '月': { '1限': '機械学習概論', '2限': 'データベース', '3限': 'Webプログラミング', '4限': null, '5限': null },
            '火': { '1限': '確率統計', '2限': 'オペレーティングシステム', '3限': '機械学習概論', '4限': null, '5限': null },
            '水': { '1限': 'データベース', '2限': 'Webプログラミング', '3限': '確率統計', '4限': null, '5限': null },
            '木': { '1限': '文化史', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '生物学', '2限': '物理学演習', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '後期',
          schedule: {
            '月': { '1限': '深層学習', '2限': 'ネットワーク', '3限': '計算機アーキテクチャ', '4限': null, '5限': null },
            '火': { '1限': '自然言語処理', '2限': '画像処理', '3限': '深層学習', '4限': null, '5限': null },
            '水': { '1限': 'ネットワーク', '2限': '計算機アーキテクチャ', '3限': '自然言語処理', '4限': null, '5限': null },
            '木': { '1限': '哲学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '化学', '2限': '地学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '前期',
          schedule: {
            '月': { '1限': 'クラウドコンピューティング', '2限': '情報セキュリティ', '3限': 'ソフトウェア工学', '4限': null, '5限': null },
            '火': { '1限': 'アルゴリズム解析', '2限': 'データサイエンス', '3限': 'クラウドコンピューティング', '4限': null, '5限': null },
            '水': { '1限': '情報セキュリティ', '2限': 'ソフトウェア工学', '3限': 'アルゴリズム解析', '4限': null, '5限': null },
            '木': { '1限': '国際関係論', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '芸術史', '2限': '音楽理論', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '後期',
          schedule: {
            '月': { '1限': 'IoTシステム開発', '2限': 'VR/AR基礎', '3限': '組込みシステム', '4限': null, '5限': null },
            '火': { '1限': 'ロボティクス', '2限': '人工知能応用', '3限': 'IoTシステム開発', '4限': null, '5限': null },
            '水': { '1限': 'VR/AR基礎', '2限': '組込みシステム', '3限': 'ロボティクス', '4限': null, '5限': null },
            '木': { '1限': '法律学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '簿記', '2限': '会計学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '前期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': 'AI倫理', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': '専門演習I', '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': 'AI倫理', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '後期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': '専門演習II', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': null, '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': '専門演習II', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        }
      ]
    },
    {
      id: 'pattern2',
      name: 'パターン2', // パターン名を通し番号に
      description: '情報セキュリティに重点を置いたバランスの取れた履修パターン',
      totalUnits: 126,
      semesters: [
        {
          year: 1, semester: '前期',
          schedule: {
            '月': { '1限': '情報科学概論', '2限': 'プログラミング基礎', '3限': '英語コミュニケーションI', '4限': '基礎物理学', '5限': null },
            '火': { '1限': '線形代数I', '2限': 'プログラミング基礎', '3限': '情報科学概論', '4限': null, '5限': null },
            '水': { '1限': '英語コミュニケーションI', '2限': '基礎物理学', '3限': '線形代数I', '4限': null, '5限': null },
            '木': { '1限': '体育', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '社会学', '2限': '経済学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 1, semester: '後期',
          schedule: {
            '月': { '1限': 'データ構造とアルゴリズム', '2限': 'ネットワーク基礎', '3限': '微積分I', '4限': null, '5限': null },
            '火': { '1限': 'コンピュータ科学', '2限': '統計学', '3限': 'データ構造とアルゴリズム', '4限': null, '5限': null },
            '水': { '1限': 'ネットワーク基礎', '2限': '微積分I', '3限': 'プログラミング演習', '4限': null, '5限': null },
            '木': { '1限': '倫理学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '心理学', '2限': '応用数学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '前期',
          schedule: {
            '月': { '1限': '情報セキュリティ概論', '2限': 'データベース', '3限': 'Webプログラミング', '4限': null, '5限': null },
            '火': { '1限': '確率統計', '2限': 'オペレーティングシステム', '3限': '情報セキュリティ概論', '4限': null, '5限': null },
            '水': { '1限': 'データベース', '2限': 'Webプログラミング', '3限': '確率統計', '4限': null, '5限': null },
            '木': { '1限': '文化史', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '生物学', '2限': '物理学演習', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '後期',
          schedule: {
            '月': { '1限': 'ネットワークプロトコル', '2限': '暗号技術', '3限': '計算機アーキテクチャ', '4限': null, '5限': null },
            '火': { '1限': 'Webセキュリティ', '2限': '画像処理', '3限': 'ネットワークプロトコル', '4限': null, '5限': null },
            '水': { '1限': '暗号技術', '2限': '計算機アーキテクチャ', '3項': 'Webセキュリティ', '4限': null, '5限': null },
            '木': { '1限': '哲学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '化学', '2限': '地学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '前期',
          schedule: {
            '月': { '1限': 'フォレンジック', '2限': '情報倫理', '3限': 'ソフトウェア工学', '4限': null, '5限': null },
            '火': { '1限': 'セキュリティ監査', '2限': 'データサイエンス', '3限': 'フォレンジック', '4限': null, '5限': null },
            '水': { '1限': '情報倫理', '2限': 'ソフトウェア工学', '3限': 'セキュリティ監査', '4限': null, '5限': null },
            '木': { '1限': '国際関係論', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '芸術史', '2限': '音楽理論', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '後期',
          schedule: {
            '月': { '1限': 'システムセキュリティ演習', '2限': '侵入テスト', '3限': 'リスク管理', '4限': null, '5限': null },
            '火': { '1限': 'データセンター設計', '2限': '人工知能応用', '3限': 'システムセキュリティ演習', '4限': null, '5限': null },
            '水': { '1限': '侵入テスト', '2限': 'リスク管理', '3限': 'データセンター設計', '4限': null, '5限': null },
            '木': { '1限': '法律学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '簿記', '2限': '会計学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '前期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': 'セキュリティ政策', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': '専門演習I', '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': 'セキュリティ政策', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '後期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': '専門演習II', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': null, '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': '専門演習II', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        }
      ]
    },
    {
      id: 'pattern3',
      name: 'パターン3', // パターン名を通し番号に
      description: 'インフラ分野に重点を置いた実践的な履修パターン',
      totalUnits: 125,
      semesters: [
        {
          year: 1, semester: '前期',
          schedule: {
            '月': { '1限': '情報科学概論', '2限': 'プログラミング基礎', '3限': '英語コミュニケーションI', '4限': '基礎物理学', '5限': null },
            '火': { '1限': '線形代数I', '2限': 'プログラミング基礎', '3限': '情報科学概論', '4限': null, '5限': null },
            '水': { '1限': '英語コミュニケーションI', '2限': '基礎物理学', '3限': '線形代数I', '4限': null, '5限': null },
            '木': { '1限': '体育', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '社会学', '2限': '経済学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 1, semester: '後期',
          schedule: {
            '月': { '1限': 'データ構造とアルゴリズム', '2限': 'ネットワーク基礎', '3限': '微積分I', '4限': null, '5限': null },
            '火': { '1限': 'コンピュータ科学', '2限': '統計学', '3限': 'データ構造とアルゴリズム', '4限': null, '5限': null },
            '水': { '1限': 'ネットワーク基礎', '2限': '微積分I', '3限': 'プログラミング演習', '4限': null, '5限': null },
            '木': { '1限': '倫理学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '心理学', '2限': '応用数学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '前期',
          schedule: {
            '月': { '1限': 'オペレーティングシステム', '2限': 'Linux基礎', '3限': 'Webプログラミング', '4限': null, '5限': null },
            '火': { '1限': '詳しい技術', '2限': 'データベース', '3限': 'クラウドコンピューティング概論', '4限': null, '5限': null },
            '水': { '1限': 'Linux基礎', '2限': 'Webプログラミング', '3限': 'オペレーティングシステム', '4限': null, '5限': null },
            '木': { '1限': '文化史', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '生物学', '2限': '物理学演習', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 2, semester: '後期',
          schedule: {
            '月': { '1限': 'コンテナ技術', '2限': 'ネットワーク設計', '3限': '計算機アーキテクチャ', '4限': null, '5限': null },
            '火': { '1限': '仮想化技術', '2限': '画像処理', '3限': 'コンテナ技術', '4限': null, '5限': null },
            '水': { '1限': 'ネットワーク設計', '2限': '計算機アーキテクチャ', '3限': '仮想化技術', '4限': null, '5限': null },
            '木': { '1限': '哲学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '化学', '2限': '地学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '前期',
          schedule: {
            '月': { '1限': 'システム運用管理', '2限': 'DevOps概論', '3限': 'ソフトウェア工学', '4限': null, '5限': null },
            '火': { '11限': '監視システム構築', '2限': 'データサイエンス', '3限': 'システム運用管理', '4限': null, '5限': null },
            '水': { '1限': 'DevOps概論', '2限': 'ソフトウェア工学', '3限': '監視システム構築', '4限': null, '5限': null },
            '木': { '1限': '国際関係論', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '芸術史', '2限': '音楽理論', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 3, semester: '後期',
          schedule: {
            '月': { '1限': 'クラウドセキュリティ', '2限': 'ネットワークセキュリティ', '3限': '組込みシステム', '4限': null, '5限': null },
            '火': { '1限': 'データセンター設計', '2限': '人工知能応用', '3限': 'クラウドセキュリティ', '4限': null, '5限': null },
            '水': { '1限': 'ネットワークセキュリティ', '2限': '組込みシステム', '3限': 'データセンター設計', '4限': null, '5限': null },
            '木': { '1限': '法律学', '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': '簿記', '2限': '会計学', '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '前期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': 'インターンシップ', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': '専門演習I', '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': 'インターンシップ', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        },
        {
          year: 4, semester: '後期',
          schedule: {
            '月': { '1限': '卒業研究', '2限': '専門演習II', '3限': null, '4限': null, '5限': null },
            '火': { '1限': null, '2限': null, '3限': '卒業研究', '4限': null, '5限': null },
            '水': { '1限': '専門演習II', '2限': null, '3限': null, '4限': null, '5限': null },
            '木': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null },
            '金': { '1限': null, '2限': null, '3限': null, '4限': null, '5限': null }
          }
        }
      ]
    }
  ];

  if (patternId) {
    const foundPattern = fullDummyPatterns.find(p => p.id === patternId);
    if (foundPattern) {
      return simulateApiCall(foundPattern);
    } else {
      return simulateApiCall(null, 500, true); // パターンが見つからない場合はエラーをシミュレート
    }
  } else {
    // 概要表示用のデータを返す (id, name, description, totalUnits のみ)
    const summaryPatterns = fullDummyPatterns.map(({ id, name, description, totalUnits }) => ({
      id, name, description, totalUnits
    }));
    return simulateApiCall(summaryPatterns);
  }
};