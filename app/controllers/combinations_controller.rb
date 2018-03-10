class CombinationsController < ApplicationController

  def create
    micropost = Micropost.find_by(id: combination_params[:micropost_id])
    if micropost
      combination_params[:tags].each do |tag|
        micropost.get_tag(tag)
      end
    end
  end

  def destroy
  end

  # Parse the accepted params
  def combination_params

  end
end
