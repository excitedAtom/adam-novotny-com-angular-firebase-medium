import { AngularFirestore, AngularFirestoreDocument } from 'angularfire2/firestore';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';

interface Item {
    title: string;
    url: string;
    paragraphs: string[];
}

@Component({
    selector: 'app-blog',
    templateUrl: './blog.component.html',
    styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {

    url = 'blog/1';
    blogDoc: AngularFirestoreDocument<Item>;
    blog: Observable<Item>;

    constructor(private db: AngularFirestore, private router: ActivatedRoute) {
    }

    ngOnInit() {
        this.router.params.subscribe((params) => {
            this.url = 'blog/' + params['name'];
        });
        this.blogDoc = this.db.doc<Item>(this.url);
        this.blog = this.blogDoc.valueChanges();
    }

}
