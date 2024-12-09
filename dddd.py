# <div class="mb-2">
#                         <label class="form-label" for="formGroupQuantitySelect">Soni:</label>
#                         <select class="form-control" name="quantity" id="formGroupQuantitySelect" required>
#                             <!-- Default value set to 1 -->
#                             {% for i in range_1_to_9 %}
#                                 <option value="{{ i }}"
#                                         {% if i == form.quantity.value|default:1 %}selected{% endif %}>{{ i }}</option>
#                             {% endfor %}
#                         </select>
#                     </div>


# < script
# src = "https://code.jquery.com/jquery-3.6.0.min.js" > < / script >
# < script
# src = "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.7/jquery.inputmask.min.js" > < / script >
# < script
# src = "https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js" > < / script >
# < link
# rel = "stylesheet"
# href = "https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" / >
#
# < script >
# $(document).ready(function()
# {
# $('#phone-mask').inputmask({
#     "mask": "+998(99) 999-99-99"
# });
# });
#
# // Initialize
# Swiper
# with Auto - Slide
#     const
#     swiper = new
#     Swiper('.mySwiper', {
#         loop: true, // Enable
#     looping
#     navigation: {
#         nextEl: '.swiper-button-next',
#         prevEl: '.swiper-button-prev',
#     },
#     pagination: {
#         el: '.swiper-pagination',
#         clickable: true,
#     },
#     autoplay: {
#                   delay: 2000, // Auto - slide
#     every
#     3
#     seconds
#     disableOnInteraction: false, // Keep
#     auto - sliding
#     even if interacted
#     },
#     });
#     < / script >
#
#     < !-- Custom
#     CSS -->
#     < style >
#     / *Make
#     the
#     description
#     images
#     fully
#     responsive * /
#     .image - uniform
#     {
#         width: 100 %; / *Ensures
#     the
#     image
#     takes
#     up
#     the
#     full
#     width
#     of
#     its
#     container * /
#     height: auto; / *Maintains
#     aspect
#     ratio * /
#     object - fit: contain; / *Ensures
#     the
#     image
#     fits
#     within
#     its
#     container
#     without
#     cropping * /
#     border - radius: 10
#     px; / *Optional: adds
#     rounded
#     corners * /
#     }
#
#     / *Adjust
#     image
#     display
#     for smaller screens * /
#         @media(max - width
#
#         : 768
#         px) {
#             .image - uniform
#         {
#             width: 100 %; / *Ensures
#         image
#         takes
#         up
#         full
#         width
#         on
#         small
#         screens * /
#         height: 80 %; / *Ensures
#         aspect
#         ratio is maintained
#         on
#         smaller
#         screens * /
#         }
#         }
#         < / style >