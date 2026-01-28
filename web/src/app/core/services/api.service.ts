import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  host = environment.apiUrl + '/';
  constructor(private http: HttpClient) {}

  //#region METHODs
  post(url: string, data: any) {
    const request = this.http.post(this.host + url, data, {
      headers: new HttpHeaders({ 'accept-language': 'EN' }),
    });
    return lastValueFrom(request) as Promise<any>;
  }

  put(url: string, data: any) {
    const request = this.http.put(this.host + url, data);
    return lastValueFrom(request) as Promise<any>;
  }

  /**
   * Upload file với FormData
   * Browser tự động set Content-Type: multipart/form-data
   */
  uploadFile(url: string, formData: FormData, reportProgress: boolean = false) {
    const options: any = {
      headers: new HttpHeaders({ 'accept-language': 'EN' }),
    };

    // Nếu muốn track progress
    if (reportProgress) {
      options.reportProgress = true;
      options.observe = 'events';
    }

    const request = this.http.post(this.host + url, formData, options);
    return lastValueFrom(request) as Promise<any>;
  }

  /**
   * Upload multiple files
   */
  uploadMultipleFiles(url: string, files: File[], fieldName: string = 'files') {
    const formData = new FormData();

    files.forEach((file, index) => {
      formData.append(`${fieldName}`, file);
    });

    const request = this.http.post(this.host + url, formData, {
      headers: new HttpHeaders({ 'accept-language': 'EN' }),
    });
    return lastValueFrom(request) as Promise<any>;
  }

  /**
   * Upload file với additional data
   */
  uploadFileWithData(
    url: string,
    file: File,
    additionalData?: any,
    fileFieldName: string = 'file',
  ) {
    const formData = new FormData();
    formData.append(fileFieldName, file);

    // Thêm các field khác vào formData
    if (additionalData) {
      Object.keys(additionalData).forEach((key) => {
        formData.append(key, additionalData[key]);
      });
    }

    const request = this.http.post(this.host + url, formData, {
      headers: new HttpHeaders({ 'accept-language': 'EN' }),
    });
    return lastValueFrom(request) as Promise<any>;
  }

  objToQueryString = (obj: any) =>
    Object.keys(obj)
      .map((k) => {
        if (Array.isArray(obj[k])) {
          return `${k}=${JSON.stringify(obj[k])}`;
        }
        return `${k}=${obj[k]}`;
      })
      .join('&');

  get(url: string): Promise<any> {
    return lastValueFrom(this.http.get(this.host + url));
  }

  //#endregion

  //#region APIs
  SESSION = {
    FIND_DETAIL: `cv-session/get-session-detail`,
  };

  FILE = {
    BEFORE_UPLOAD: `files/upload`,
    SCAN_CV: `files/scan-cv`,
  };
  //#endregion
}
