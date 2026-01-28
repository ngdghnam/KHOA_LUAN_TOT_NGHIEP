import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { LoadingConfig, LoadingService } from '../../core/services/loading.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.css'],
  imports: [CommonModule],
})
export class LoadingComponent implements OnInit, OnDestroy {
  isLoading = false;
  config: LoadingConfig = {
    message: 'Đang tải...',
    imageUrl: 'assets/images/loading.gif',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    zIndex: 9999,
  };

  private destroy$ = new Subject<void>();

  constructor(private loadingService: LoadingService) {}

  ngOnInit(): void {
    // Subscribe to loading state
    this.loadingService.loading$.pipe(takeUntil(this.destroy$)).subscribe((loading) => {
      this.isLoading = loading;
    });

    // Subscribe to config changes
    this.loadingService.config$.pipe(takeUntil(this.destroy$)).subscribe((config) => {
      this.config = config;
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
