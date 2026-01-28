import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface LoadingConfig {
  message?: string;
  imageUrl?: string;
  backgroundColor?: string;
  zIndex?: number;
}

@Injectable({
  providedIn: 'root',
})
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  private configSubject = new BehaviorSubject<LoadingConfig>({
    message: 'Đang tải...',
    imageUrl: 'assets/images/loading.gif', // ← THAY ĐỔI ĐƯỜNG DẪN HÌNH ẢNH TẠI ĐÂY
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    zIndex: 9999,
  });

  public loading$: Observable<boolean> = this.loadingSubject.asObservable();
  public config$: Observable<LoadingConfig> = this.configSubject.asObservable();

  constructor() {}

  /**
   * Hiển thị loading
   */
  show(config?: LoadingConfig): void {
    if (config) {
      this.configSubject.next({
        ...this.configSubject.value,
        ...config,
      });
    }
    this.loadingSubject.next(true);
  }

  /**
   * Ẩn loading
   */
  hide(): void {
    this.loadingSubject.next(false);
  }

  /**
   * Cập nhật message trong lúc loading
   */
  updateMessage(message: string): void {
    this.configSubject.next({
      ...this.configSubject.value,
      message,
    });
  }

  /**
   * Cập nhật hình ảnh loading
   */
  updateImage(imageUrl: string): void {
    this.configSubject.next({
      ...this.configSubject.value,
      imageUrl,
    });
  }

  /**
   * Reset về config mặc định
   */
  resetConfig(): void {
    this.configSubject.next({
      message: 'Đang tải...',
      imageUrl: 'assets/images/loading.gif', // ← THAY ĐỔI ĐƯỜNG DẪN HÌNH ẢNH TẠI ĐÂY
      backgroundColor: 'rgba(0, 0, 0, 0.7)',
      zIndex: 9999,
    });
  }
}
