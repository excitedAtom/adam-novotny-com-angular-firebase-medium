import { AngularFirestore } from 'angularfire2/firestore';
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
    blog: Observable<any[]>;
    quotes: any[] = [];
    quotesUrl = 'https://spreadsheets.google.com/feeds/list/1g6UwXwvHwpAQcNwkrR5CszdU2eIEDP02y1OGr3V5H40/od6/public/basic?alt=json';
    randomQuoteIdx: number[] = [];

    constructor(db: AngularFirestore, private http: HttpClient) {
        this.blog = db.collection('blog', ref => ref.orderBy('date_unix', 'desc'))
            .valueChanges();
    }

    ngOnInit() {
        this.http.get(this.quotesUrl).subscribe(
            (data) => {
                this.formatQuotes(data);
                this.generateRandomIdx();
            }
        );
    }

    formatQuotes(data) {
        /*
        Reformates and scrapes data json data object and saves relevant
        information as this.quotes
        data: json object from this.quotesUrl
        */
        const quotesRaw = data['feed']['entry'];
        quotesRaw.forEach(element => {
            const quote = element['title']['$t'].trim();
            let author = '';
            let url = '';
            const content = element['content']['$t'].split(',');
            content.forEach(c => {
                const contentTuple = c.split(':');
                const contentType = contentTuple[0].trim();
                if (contentType === 'author') {
                    author = contentTuple[1].trim();
                } else if (contentType === 'url') {
                    // combine https + url
                    url = contentTuple[1].trim() + ':' + contentTuple[2].trim();
                }
            });
            this.quotes.push({'quote': quote, 'author': author, 'url': url});
        });
    }

    generateRandomIdx() {
        /*
        Generates random array of < x numbers
        */
        this.randomQuoteIdx = [];
        for (let i = 0; i < 1; i++) {
            let number = Math.floor(Math.random() * (this.quotes.length - 1));
            while (this.randomQuoteIdx.includes(number)) {
                number = Math.floor(Math.random() * (this.quotes.length - 1));
            }
            this.randomQuoteIdx.push(number);
        }
    }
}
