import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../../core/services/api.service';
import { ActivatedRoute, Router } from '@angular/router';

interface QuestionData {
  questions: string[];
  summarize: string;
}

@Component({
  selector: 'app-answer-question',
  templateUrl: './answer-question.component.html',
  styleUrls: ['./answer-question.component.css'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatProgressSpinnerModule,
  ],
})
export class AnswerQuestionComponent implements OnInit, OnDestroy {
  sessionId: string = '';
  questions: string[] = [];
  form!: FormGroup;

  // Polling state
  isPolling = true; // đang chờ AI agent trả về questions
  pollingStatus = 'AI đang phân tích CV của bạn. Hãy chuẩn bị để phỏng vấn';
  private pollingInterval: any = null;
  private maxRetries = 30; // 30 lần x 3s = tối đa 90s chờ
  private retryCount = 0;

  // Submit state
  isSubmitting = false;
  isSubmitPolling = false;
  submitPollingStatus = '';
  private submitPollingInterval: any = null;
  private submitRetryCount = 0;
  private submitMaxRetries = 20;

  currentRound: number = 1;
  maxRound: number = 2;

  dataObject: any = {};
  questionsR1: string[] = [];
  answersR1: string[] = [];

  questionsR2: string[] = [];
  answersR2: string[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private fb: FormBuilder,
    private apiService: ApiService,
  ) {}

  ngOnInit(): void {
    this.sessionId = this.route.snapshot.paramMap.get('id') ?? '';
    this.form = this.fb.group({});
    this.startPollingForQuestions();
  }

  startPollingForQuestions(): void {
    this.pollingInterval = setInterval(() => {
      this.retryCount++;

      if (this.retryCount > this.maxRetries) {
        this.stopPollingForQuestions();
        this.pollingStatus = 'Quá thời gian chờ. Vui lòng thử lại.';
        this.isPolling = false;
        return;
      }

      this.getAllData();
    }, 3000);
  }

  getAllData(): void {
    this.apiService.get(`${this.apiService.SESSION.FIND_DETAIL}/${this.sessionId}`).then((res) => {
      if (res?.data?.questions?.length > 0) {
        this.stopPollingForQuestions();

        this.dataObject = res.data;
        console.log(this.dataObject);

        const sortedQuestions = res.data.questions
          .sort((a: any, b: any) => a.order_index - b.order_index)
          .map((q: any) => q.content);

        this.questions = sortedQuestions;

        this.questionsR1 = [...sortedQuestions];

        this.buildForm();
        this.isPolling = false;
      }
    });
  }

  stopPollingForQuestions(): void {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
  }

  // ==================== BUILD FORM ====================

  buildForm(): void {
    const controls: Record<string, any> = {};
    this.questions.forEach((_, index) => {
      controls[`answer_${index}`] = ['', Validators.required];
    });
    this.form = this.fb.group(controls);
  }

  getControl(index: number) {
    return this.form.get(`answer_${index}`);
  }

  // ==================== SUBMIT + POLLING RESULT ====================

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;

    const formattedAnswers: string[] = this.questions.map(
      (_, index) => this.form.value[`answer_${index}`],
    );

    // ================= ROUND 1 =================
    if (this.currentRound === 1) {
      // Lưu answers round 1
      this.answersR1 = [...formattedAnswers];

      const payload = {
        session_id: this.sessionId,
        questions: this.questionsR1,
        answers: this.answersR1,
      };

      this.apiService
        .post(this.apiService.SESSION.SUBMIT_TO_GET_OTHER, payload)
        .then((res) => {
          const newQuestions = res?.questions || res?.data?.questions;

          if (newQuestions?.length > 0) {
            this.questions = newQuestions;

            // Lưu round 2 questions
            this.questionsR2 = [...newQuestions];

            this.buildForm();
            this.currentRound = 2;

            window.scrollTo({ top: 0, behavior: 'smooth' });
          }

          this.isSubmitting = false;
        })
        .catch((err) => {
          console.error(err);
          this.isSubmitting = false;
        });

      return;
    }

    // ================= ROUND 2 =================
    if (this.currentRound === 2) {
      // Lưu answers round 2
      this.answersR2 = [...formattedAnswers];

      const finalPayload = {
        session_id: this.sessionId,

        questionsR1: this.questionsR1,
        answersR1: this.answersR1,

        questionsR2: this.questionsR2,
        answersR2: this.answersR2,

        summary: this.dataObject?.summary,
      };

      console.log('FINAL PAYLOAD:', finalPayload);

      this.apiService
        .post(this.apiService.SESSION.FINALIZE, finalPayload)
        .then(() => {
          this.isSubmitting = false;
          this.router.navigate(['/analysed-session-result', this.sessionId]);
        })
        .catch((err) => {
          console.error(err);
          this.isSubmitting = false;
        });
    }
  }

  startPollingForResult(): void {
    this.isSubmitPolling = true;
    this.submitPollingStatus = 'Đang phân tích câu trả lời...';

    this.submitPollingInterval = setInterval(() => {
      this.submitRetryCount++;

      if (this.submitRetryCount > this.submitMaxRetries) {
        this.stopPollingForResult();
        this.submitPollingStatus = 'Quá thời gian chờ. Vui lòng thử lại.';
        this.isSubmitting = false;
        return;
      }

      this.checkResultReady();
    }, 3000);
  }

  checkResultReady(): void {
    this.apiService.get(`${this.apiService.SESSION.FIND_DETAIL}/${this.sessionId}`).then((res) => {
      if (res && res.status === 'DONE') {
        this.stopPollingForResult();
        this.router.navigate(['/analysed-session-result', this.sessionId]);
      }
    });
  }

  stopPollingForResult(): void {
    if (this.submitPollingInterval) {
      clearInterval(this.submitPollingInterval);
      this.submitPollingInterval = null;
    }
    this.isSubmitPolling = false;
  }

  // ==================== CLEANUP ====================

  ngOnDestroy(): void {
    this.stopPollingForQuestions();
    this.stopPollingForResult();
  }
}
