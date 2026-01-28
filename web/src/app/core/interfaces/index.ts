export interface CVAnalysisData {
  success: boolean;
  data: CVAnalysisDetail;
}

export interface CVAnalysisDetail {
  cv_file_id: string;
  is_deleted: boolean;
  user_id: string | null;
  deleted_at: string | null;
  status: string;
  created_by: string | null;
  summary: string;
  updated_by: string | null;
  completed_at: string;
  id: string;
  created_at: string;
  updated_at: string;
  questions: Question[];
  article_recommendations: ArticleRecommendation[];
  skill_gaps: SkillGap[];
}

export interface Question {
  content: string;
  order_index: number;
  created_at: string;
  is_deleted: boolean;
  created_by: string | null;
  id: string;
  session_id: string;
  updated_at: string;
  deleted_at: string | null;
  updated_by: string | null;
}

export interface ArticleRecommendation {
  session_id: string;
  url: string;
  priority: number | null;
  created_at: string;
  is_deleted: boolean;
  created_by: string | null;
  article_id: string | null;
  title: string;
  reason: string | null;
  id: string;
  updated_at: string;
  deleted_at: string | null;
  updated_by: string | null;
}

export interface SkillGap {
  session_id: string;
  learning_keyword: string;
  why_it_matters: string;
  created_at: string;
  is_deleted: boolean;
  created_by: string | null;
  skill_gap: string;
  id: string;
  updated_at: string;
  deleted_at: string | null;
  updated_by: string | null;
  resource_types: ResourceType[];
}

export interface ResourceType {
  created_at: string;
  skill_gap_id: string;
  is_deleted: boolean;
  created_by: string | null;
  resource_type: string;
  id: string;
  updated_at: string;
  deleted_at: string | null;
  updated_by: string | null;
}

export interface SummarySection {
  title: string;
  content: string;
  type: 'profile' | 'strengths' | 'weaknesses' | 'risks' | 'conclusion';
}
