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
        "format_src": "tewwg.json"
    },
    "thecolony":{
      "title": "The Colony",
      "book_src": "/thecolony.pdf",
      "names": "James,Lloyd,Masson,mair\u00e9ad, Francis",
      "format_src": "thecolony.json"
    },
    "unbearable_lightness":{
      "title": "The Unbearable Lightness of Being",
      "book_src": "/unbearable_lightness.pdf",
      "names": "Tereza,Tomas,Sabina,Simon,Franz",
      "format_src": "unbearable_lightness.json",
    },
    "little_women":{
      "title": "Little Women",
      "book_src": "/little_women_book_1.pdf",
      "names":"Jo,Meg,Beth,Amy,Laurie",
      "format_src": "little_women.json"
    },
    "persuasion":{
      "title": "Persuasion",
      "book_src": "/persuasion.pdf",
      "names":"Anne, Captain Wentworth, Sir Walter, Admiral Croft, Elizabeth, Mary, Charles Musgrove, Elliot, Charles Hayter, Captain Benwick, Smith, Louisa Musgrove, Captain Harville, Mr Musgrove, Mrs Musgrove, Henrietta Musgrove, Lady Russell, Miss Hamilton, Mrs Croft",
      "format_src": "persuasion.json"
    },
    "remains_of_the_day":{
      "title": "The Remains of the Day",
      "book_src": "/remains_of_the_day.pdf",
      "names":"Stevens, Miss Kenton, Lord Darlington, Mr Farraday, Mr Cardinal, Mr Spencer, Mr Taylor, Mr Graham, Mr Smith, Mr Stevens, Mr Marshall, Mr Lane, Mr Benn",
      "format_src": "remains_of_the_day.json"
    }
}
export function generateStaticParams() {
  return [
    { bookname: "exit_west" },
    { bookname: "pride_and_prejudice" },
    { bookname: "tewwg" },
    { bookname: "thecolony"},
    { bookname: "unbearable_lightness"},
    { bookname: "little_women"},
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
