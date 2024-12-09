import GeneralBookPage from "@/components/generalBookPage";

// Return a list of `params` to populate the [slug] dynamic segment
type BookInfo = {
    title: string;
    book_src: string;
    names: string;
    format_src: string;
  };
const books: { [id: string]: BookInfo; } = {
    "exit_west": {
        "title": "Exit West",
        "book_src": "/exit_west_textfile.txt",
        "names": "Nadia,Saeed",
        "format_src": "exit_west_textfile.txt"
    },
    "pride_and_prejudice": {
        "title" : "Pride and Prejudice",
        "book_src": "/p&p_textfile.txt",
        "names": "Bingley, Jane, Elizabeth, Lydia, Bennet, Darcy, Wickham, Gardiner, Lucas, Collins, Charlotte, Catherine, de Bourgh",
        "format_src": "p%26p_textfile.txt"
    },
    "tewwg": {
        "title": "Their Eyes Were Watching God",
        "book_src": "/tewwg.pdf",
        "names": "Janie,Joe,Logan,Pheoby,Nanny",
        "format_src": "tewwg.docx"
    }
}
export function generateStaticParams() {
  return [
    { bookname: "exit_west" },
    { bookname: "pride_and_prejudice" },
    { bookname: "tewwg" },
  ];
}
// Multiple versions of this page will be statically generated
// using the `params` returned by `generateStaticParams`
export default async function Page({
  params,
}: {
  params: { bookname: string };
}) {
  const bookname  = await params.bookname;
  const bookData = books[bookname];
  return (
    <div>
       <GeneralBookPage bookSrc={bookData.book_src} names={bookData.names} formatSrc={bookData.format_src}/>
    </div>
  )
}
