import { CommonModule, NgClass } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css'],
  imports: [
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatTooltipModule,
    MatSelectModule,
    CommonModule,
  ],
})
export class FooterComponent implements OnInit {
  studyImages: string[] = [];

  constructor() {}

  ngOnInit() {
    this.onGetStudyImage();
  }

  onGetStudyImage() {
    for (let i = 1; i <= 6; i++) {
      this.studyImages.push(`assets/imgs/study${i}.jpg`);
    }
  }
}
