import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  API_URL = "http://127.0.0.1:5000";

  // @ViewChild('wordd') myword: ElementRef
  // @ViewChild('threshold') mythreshold: ElementRef
  // @ViewChild('numberresults') mynumber_results: ElementRef;

  myword = 'dog';
  mythreshold = .9;
  mynumberresults = 15;
  results: string[] = [];

  constructor(private http: HttpClient){
  };

  getRhymes(word:string, thres:number, numres:number){
    this.results = [];
    this.http.get<any>(`${this.API_URL}/rhymes/${word}/${thres}/${numres}`).subscribe(res=>{
      for(let item of res){
        this.results.push("Word: " + item.word + ",  Score: " + item.score + "\n")
      }
    })
    
  }

  ngOnInit(): void {}
}
