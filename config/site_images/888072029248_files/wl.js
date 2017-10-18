//Wishlist functions
$(document).ready(function(){
	
if( $(".ss_wl_shareurl").size() > 0 ){
	$(".ss_wl_emailshare").css("display", "inline");
	
	var values = $.trim( $("#wl_emailshare input[name='firstname']").val() ).split(" ");
	var firstname = values[0];
	
	$("#wl_emailshare input[name='firstname']").val( firstname );
	$("#wl_emailshare input[name='url']").val( $(".ss_wl_shareurl input").val() );
	$("#wl_emailshare input[name='subject']").val( firstname + "'s Wish List At SoundStageDirect.com" );
	$("#wl_emailshare textarea[name='content']").val( firstname + " - has sent you their wish list via SoundStageDirect.\n\nCheck out my SoundStageDirect wish list! I've been keeping a list of the items I've had my eye on to make it easy for friends and family to get me the gifts I really want.\n\nThanks for looking.\n\n" + firstname );
	$("#wl_emailshare a.viewlist").attr("href", $(".ss_wl_shareurl input").val() ).text("View " + firstname + "'s wish list");
	
	var subjectUpdated = false;
	$("#wl_emailshare textarea[name='content']").change(function(){subjectUpdated = true})
	$("#wl_emailshare input[name='from']").on("change keyup keypress keydown", function(){
		if(subjectUpdated == false){
			$("#wl_emailshare textarea[name='content']").val( firstname + " - " + $(this).val() + " - has sent you their wish list via SoundStageDirect.\n\nCheck out my SoundStageDirect wish list! I've been keeping a list of the items I've had my eye on to make it easy for friends and family to get me the gifts I really want.\n\nThanks for looking.\n\n" + firstname );
		}
	})
	
	$("#wl_emailshare").popup();
	$("#wl_emailshare .close").click(function(){
		$("#wl_emailshare").popup("hide");
	});
	$(".ss_wl_emailshare img").click(function(){
		subjectUpdated = false;
		$("#wl_emailshare").popup("show");
	})
	$("#wl_emailshare form").validate({submitHandler: function(form){
		$(form).addClass("loading");
		$.ajax({
			type: $(form).attr("method"),
			url: $(form).attr("action"),
			data: $(form).serialize(),
			success: function(msg){
				$(form).removeClass("loading");
				$("#wl_emailshare").popup("hide");
				alert(msg); 
			},
			error: function(){
				$(form).removeClass("loading");
				alert("Something wrong. Please try again later.")
			}
		});		
	}});
}
	
	$(".create-wishlist-link span.createwishlist a, .unused-text-button span.createwishlist a").click(function(event){
		$("#createwishlistfrm").popup("show");
		event.preventDefault();
	});
	
	$("#createwishlistfrm span.close, #createwishlistfrm input[value='Continue Shopping']").click(function(event){
		$("#createwishlistfrm").popup("hide");
		event.preventDefault();
	})
	
	if($("div.addtowishlist").size() > 0){
		
		if(authorized()){
		
			var url = baseCgiUrl + '/wishlist.cgi?callback=wishlist&storeid=' + storeId + '&func=gl&_=' + Math.random();
			
			$.ajax(url, {
				complete: function(response){
					var txt = response.responseText;
					txt = txt.substring(15);
					txt = txt.substring(0, txt.length - 3);
					eval('var wishlist =' + txt);
					
					html = "<ul>";
					for(var i = 0; i < wishlist.length; i++){
						html += '<li wishlistid="' + wishlist[i].id + '">';
						html += wishlist[i].name + "<span>" + wishlist[i].priv + "</span>";
						html += "</li>";
					}
					html += "<li>Create new Wish List</li>"
					html += "</ul>";
					
					$("div.addtowishlist").append(html)

					$("div.addtowishlist").each(function(index, div){
				
						$(div).hover(function(){
							$(this).find("ul").slideDown();
						}).mouseleave(function(){
							$(this).find("ul").stop(true, true).slideUp();
						})
						
						$(div).find("li").click(function(){
						
							var id = $(this).parent().parent().attr("id").substring(9);
							if($(this).html() == "Create new Wish List"){
							
								$("#createwishlistfrm input[name='itemnum']").attr("disabled", null).val( $(".product-info input[name='itemnum']").val() );
								var url = document.location.href;
								var index = url.indexOf("?");
								if(index > 0){
									url = url.substring(0, index);
								}
								url += "?itemnum=" + $(".product-info input[name='itemnum']").val();
							
								$("#createwishlistfrm input[name='addedfrom']").attr("disabled", null).val(url);
								$("#createwishlistfrm input[name='qnty']").attr("disabled", null).val($(".product-info .qty input[type='text']").val());
								
								$("#createwishlistfrm").popup("show");

								
							}else{
								document.location.href = baseCgiUrl + '/wishlist.cgi?func=add&itemnum=' + id + '&storeid=' + storeId + '&wl=' + $(this).attr("wishlistid");
							}
						})
					})
					
					if(window.location.href.indexOf("wishlist=1") > 0){
						if(wishlist.length == 0){
							$("#createwishlistfrm input[name='itemnum']").attr("disabled", null).val( $(".product-info input[name='itemnum']").val() );
							var url = document.location.href;
							var index = url.indexOf("?");
							if(index > 0){
								url = url.substring(0, index);
							}
							url += "?itemnum=" + $(".product-info input[name='itemnum']").val();
							
							$("#createwishlistfrm input[name='addedfrom']").attr("disabled", null).val(url);
							$("#createwishlistfrm input[name='qnty']").attr("disabled", null).val( $(".product-info .qty input[type='text']").val() );
								
							$("#createwishlistfrm").popup("show");
						}else{
							$("div.addtowishlist ul").show();
						}
					}
					
				}
			})
			
		
		}else{//not log 
			$("div.addtowishlist").click(function(){
				var id = $(this).attr("id").substring(9);
				document.location.href = baseCgiUrl + '/order.cgi?storeid=' + storeId + '&itemnum=' + id + '&wl=cr&func=2&html_reg=html';
			})		
		}
	}	
	
	$("span.editwishlist a").click(function(event){
		var vars = {};
		var parts = this.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
   			vars[key] = value;
   		});
			
		var wlid = vars["wl"];
		$("#editwishlistfrm input[name='wl']").val(wlid);
		
		$.ajax({
    		url: baseCgiUrl + "/wishlist.cgi" + $(this).attr("href"),
    		type: "get",
    		
    		success: function(response){

				var html = $(response);
				
				if(html.find("input[name='name']").size() > 0){
					var name = html.find("input[name='name']").val();
				}else{
					var name = "";
				}
					
				$("#editwishlistfrm input[name='name']").val(name).focus();
					
				if(html.find("textarea[name='comments']").size() > 0){
					var comments = html.find("textarea[name='comments']").val();
				}else{
					var comments = "";
				}
					
				$("#editwishlistfrm textarea[name='comments']").val(comments);
					
				if(html.find("select[name='priv']").size() > 0){
					var pri = html.find("select[name='priv']").val();
				}else{
					var pri = "";
				}
					
				$("#editwishlistfrm select[name='priv']").val(pri);
					
				$("#editwishlistfrm").popup("show");
			}
		})
		event.preventDefault();
	})
	
	$("#editwishlistfrm span.close, #editwishlistfrm input[value='Continue Shopping']").click(function(event){
		$("#editwishlistfrm").popup("hide");
	})
	
	$(".unused-text-button span.deletewishlist a").click(function(event){
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
     			vars[key] = value;
   		});
			
		var wlid = vars["wl"];
			
		$("#deletewishlistfrm input[name='wl']").val(wlid);
		
		$("#deletewishlistfrm").popup("show")
			
		event.preventDefault();
		return false;
	})
	$("#deletewishlistfrm span.close, #deletewishlistfrm input[value='No ']").click(function(event){
		$("#deletewishlistfrm").popup("hide");
		event.preventDefault();
	})
	
	
	//fixing problem with quantity
	$(".wishlist-product-options form").submit(function(event){
		var itemnum = $(this).find("input[name='itemnum']").val();
		if( $(this).parent().parent().find("input[name='qntyDesired']") > 0){
			var qnty = $(this).parent().parent().find("input[name='qntyDesired']").val();
		}else{
			var qnty = 1;
		}
		
		$(this).append('<input type="hidden" name="' + itemnum + ':qnty" value="'+qnty+'" />');
		
	})
	
	if($(".wishlist-product-options form").size() > 0){	
		//auto saving information about product inside wishlist	
		
		$("form.wl_prod_info input[type='text']").keypress(function(){
			$(this).closest("form").find(".saved").hide();
		})
		
		$("form.wl_prod_info input[type='text'], form.wl_prod_info select").change(function(){
			var form = $(this).closest("form");
			
			if(form.find(".saved").size() == 0){
				form.find(".ss_wl_qnty").append('<div class="saved">Saving</div>');
			}
			form.find(".saved").text("Saving...").show();
			$.ajax({
			
				url: form.attr("action"),
				type: form.attr("method"),
				data: form.serialize(),
				success: function(response){
					form.find(".saved").text("Saved!").show();
				}
			});
		})
		
		
		//adding "Add all products to cart"		
		if( $("a.menu-link:visible").size() > 0 ){
			$("#wishlist-products").append('<input type="button" id="addalltocart" value="Add All Items to the Basket!" />');
		}else{
			$("#wishlist-products").append('<input type="button" id="addalltocart" value="Add All Products on the page to the Basket!" />');
		}
		$("#wishlist-products").append('<form method="post" action="' + baseCgiUrl + '/order.cgi" id="addalltocartfrm" style="display: none;"><input type="hidden" name="storeid" value="' + storeId + '"><input type="hidden" name="dbname" value="products"><input type="hidden" name="function" value="add"></form>		');
	
		$("#addalltocart").click(function(){
		
			$(".wishlist-product-options form").each(function(index, form){
				var itemnum = $(form).find("input[name='itemnum']").val();
				var qnty = $(form).closest("div.wishlist-product").find("input[name='qntyDesired']").val();
				var wlpid = $(form).find("input[name='" + itemnum + ":wlpid']").val();

				$("#addalltocartfrm").append('<input type="hidden" name="itemnum" value="' + itemnum + '" />');
		
				$("#addalltocartfrm").append('<input type="hidden" name="' + itemnum + ':qnty" value="'+qnty+'" />');
			
				$("#addalltocartfrm").append('<input type="hidden" name="' + itemnum + ':wlpid" value="'+wlpid+'" />');
			})
		
			$("#addalltocartfrm").submit();
		})
	
	}
})