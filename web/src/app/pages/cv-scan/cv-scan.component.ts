import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../core/services/api.service';
import { LoadingService } from '../../core/services/loading.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cv-scan',
  templateUrl: './cv-scan.component.html',
  styleUrls: ['./cv-scan.component.css'],
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
  ],
})
export class CvScanComponent implements OnInit {
  selectedFile: File | null = null;
  isDragging = false;
  uploading = false;
  uploadProgress = 0;

  readonly maxFileSize = 5 * 1024 * 1024; // 5MB
  readonly acceptedFormats = ['.pdf', '.doc', '.docx'];
  readonly acceptedMimeTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ];

  dataObject: any = {};
  sessionObject: any = {};

  constructor(
    private snackBar: MatSnackBar,
    private readonly apiService: ApiService,
    private loadingService: LoadingService,
    private readonly router: Router,
  ) {}

  ngOnInit() {}

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.handleFile(input.files[0]);
    }
  }

  handleFile(fileUpload: File): void {
    // Validate file type
    if (!this.acceptedMimeTypes.includes(fileUpload.type)) {
      this.snackBar.open('Chỉ chấp nhận file PDF, DOC, DOCX', 'Đóng', {
        duration: 3000,
        panelClass: ['error-snackbar'],
      });
      return;
    }

    // Validate file size
    if (fileUpload.size > this.maxFileSize) {
      this.snackBar.open('File không được vượt quá 5MB', 'Đóng', {
        duration: 3000,
        panelClass: ['error-snackbar'],
      });
      return;
    }

    this.selectedFile = fileUpload;

    // Tạo FormData
    const formData = new FormData();
    formData.append('file', this.selectedFile);

    // Sử dụng method uploadFile
    this.apiService.uploadFile(this.apiService.FILE.BEFORE_UPLOAD, formData).then((res) => {
      this.snackBar.open('Upload file thành công', 'Đóng', {
        duration: 2000,
        panelClass: ['success-snackbar'],
      });
      console.log('res', res.filename);
      console.log('res', res.object_name);

      this.dataObject.cv_name = res.object_name;

      // ANALYSED DATA
      this.analyseCv(this.dataObject);
    });
  }

  analyseCv(data: any) {
    this.apiService.post(this.apiService.FILE.SCAN_CV, data).then((res) => {
      // console.log(res);
      this.loadingService.show();
      if (res) {
        this.sessionObject.session_id = res.session_id;
        this.router.navigate(['/analysed-session-result', this.sessionObject.session_id]);
        this.loadingService.hide();
      }
    });
  }

  removeFile(): void {
    this.selectedFile = null;
    this.uploadProgress = 0;
  }

  uploadFile(): void {
    if (!this.selectedFile) return;

    this.uploading = true;
    this.uploadProgress = 0;

    // Thực tế bạn sẽ gọi API upload ở đây
    // this.cvService.uploadCV(this.selectedFile).subscribe(...)
  }

  getFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  getFileIcon(fileName: string): string {
    if (fileName.endsWith('.pdf')) return 'picture_as_pdf';
    if (fileName.endsWith('.doc') || fileName.endsWith('.docx')) return 'description';
    return 'insert_drive_file';
  }
}
