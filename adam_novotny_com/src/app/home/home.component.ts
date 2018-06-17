import { AngularFirestore } from 'angularfire2/firestore';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

    blog: Observable<any[]>;

    constructor(db: AngularFirestore) {
        this.blog = db.collection('blog', ref => ref.orderBy('date_unix', 'desc'))
            .valueChanges();
    }

    ngOnInit() {
    }
}
