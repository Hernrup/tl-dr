export class Post {
    id: string
    title: string;
    date: string;
    image: string;
    body: string

    constructor(title: string, body: string){
        this.title = title;
        this.body = body;
    }
}
