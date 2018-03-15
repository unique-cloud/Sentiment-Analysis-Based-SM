class MatchingsController < ApplicationController

  def index
    micropost = Micropost.find(params[:micropost_id])
    return if micropost.nil?

    users_with_common_tags = []
    micropost.tags.each do |tag|
      tag.users.each do |user|
        users_with_common_tags.push([user, tag])
      end
    end
    # delete the owner of the micropost
    author = micropost.user
    users_with_common_tags.delete_if { |k| k.first == author }

    @matching_users = users_with_common_tags.inject(Hash.new { |h,k| h[k] = []}){ |h,v| h[v[0]] = h[v[0]] << v[1]; h }
    @matching_users = @matching_users.sort_by { |k,v| v.count }.reverse
    # @matching_users = @matching_users.paginate(page: params[:page])
  end

  def show
    @user = User.find(params[:user_id])
    tag = Tag.find(params[:tag_id])
    @microposts = @user.microposts
    @microposts = @microposts.select { |m| m.tags.include?(tag) }
    @total = @microposts.count
    @microposts = @microposts.paginate(page: params[:page])
    render 'users/show'
  end
end
