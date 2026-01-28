import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pages/landing/landing.component').then((m) => m.LandingComponent),
  },
  {
    path: 'scan-cv',
    loadComponent: () => import('./pages/cv-scan/cv-scan.component').then((m) => m.CvScanComponent),
  },
  {
    path: 'analysed-session-result/:id', // 👈 BẮT BUỘC
    loadComponent: () =>
      import('./pages/results/results.component').then((m) => m.ResultsComponent),
  },
];
