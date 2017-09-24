import { Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import { Post} from '../post';
import { PostService } from '../post.service';

@Component({
    selector: 'post-list-item',
    templateUrl: './post-list-item.component.html',
    styleUrls: ['./post-list-item.component.scss']
})
export class PostListItemComponent implements OnInit {

    @Input()
    post: Post = null;

    error: any;


    constructor(
        private postService: PostService
    ) { }

    ngOnInit() {
    }
}

