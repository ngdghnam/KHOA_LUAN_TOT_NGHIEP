import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ActivatedRoute } from '@angular/router';
import { interval, Subscription, switchMap, takeWhile, startWith } from 'rxjs';
import { ApiService } from '../../core/services/api.service';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css'],
  imports: [
    MatCardModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatDividerModule,
    MatListModule,
    MatIconModule,
    CommonModule,
  ],
})
export class ResultsComponent implements OnInit, OnDestroy {
  sessionId!: string;
  session: any;
  loading = true;
  pollingSub?: Subscription;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private sanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.sessionId = this.route.snapshot.paramMap.get('id')!;
    this.startPolling();
  }

  startPolling() {
    this.pollingSub = interval(3000)
      .pipe(
        startWith(0), // Gọi ngay lập tức thay vì đợi 3s đầu tiên
        switchMap(() => this.apiService.get(`cv-session/get-session-detail/${this.sessionId}`)),
        takeWhile((res: any) => {
          // Kiểm tra cả trường hợp res.data null hoặc status chưa DONE
          return !res.data || res.data.status !== 'DONE';
        }, true),
      )
      .subscribe({
        next: (res: any) => {
          if (res.data) {
            this.session = res.data;
            this.loading = res.data.status !== 'DONE';
          } else {
            // Session chưa có data, vẫn đang processing
            this.loading = true;
          }
        },
        error: (err) => {
          console.error('Polling error:', err);
          this.loading = false;
        },
      });
  }

  ngOnDestroy(): void {
    this.pollingSub?.unsubscribe();
  }

  getDomain(url: string): string {
    try {
      const domain = new URL(url).hostname;
      return domain.replace('www.', '');
    } catch {
      return 'Unknown';
    }
  }

  formatSummary(markdown: string): SafeHtml {
    if (!markdown) return '';

    let html = markdown
      // Headers (## -> h2, ### -> h3)
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')

      // Bold text (**text** or __text__)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/__(.*?)__/g, '<strong>$1</strong>')

      // Italic text (*text* or _text_)
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/_(.*?)_/g, '<em>$1</em>')

      // Unordered lists (* item)
      .replace(/^\* (.*$)/gim, '<li>$1</li>')

      // Wrap lists in <ul>
      .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')

      // Fix multiple <ul> tags (merge consecutive lists)
      .replace(/<\/ul>\s*<ul>/g, '')

      // Paragraphs (lines not starting with special chars)
      .split('\n\n')
      .map((paragraph) => {
        if (!paragraph.trim()) return '';
        if (paragraph.match(/^<(h[1-6]|ul|li)/)) return paragraph;
        return `<p>${paragraph}</p>`;
      })
      .join('\n');

    return this.sanitizer.sanitize(1, html) || '';
  }
}
