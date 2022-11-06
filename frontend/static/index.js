function toggle_display() {
  add_playlist_btn = document.querySelector('.add_playlist');
  add_queue_btn = document.querySelector('.add_queue');
  pl_text = document.querySelector('.playlist_text');
  pl_input = document.querySelector('.playlist_input');
  pl_input.setAttribute('required', '');
  pl_text.style.display = 'block';



}

function enqueue() {
  add_playlist_btn = document.querySelector('.add_playlist');
  add_queue_btn = document.querySelector('.add_queue');
  pl_text = document.querySelector('.playlist_text');
  pl_input = document.querySelector('.playlist_input');

  pl_input.removeAttribute('required');
  pl_text.style.display = 'none';

}
