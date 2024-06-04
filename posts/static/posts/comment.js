const commentPost = () => {
  const commentForms = [...document.getElementsByClassName("comment-form")];
  commentForms.forEach((form) =>
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const post_id = form.getAttribute("post-id");
      const commentInput = document.getElementById(`input-comment-${post_id}`);
      const commentLink = document.getElementById(`comments-${post_id}`);

      $.ajax({
        type: "POST",
        url: "/posts/comments/new/",
        data: {
          csrfmiddlewaretoken: csrftoken,
          pk: post_id,
          commentData: commentInput.value,
        },
        success: function (response) {
          $(`#comments-${post_id}`).prepend(response.comment_template);
          commentInput.value = "";
        },
        error: function (xhr, status, error) {          
          const responseJson = xhr.responseJSON;
          if (responseJson && responseJson.error) {
            alert(responseJson.error);
          } else {
            alert("An error occurred while posting the comment. Please try again later.");
          }
        },
      });
    })
  );
};

commentPost();
