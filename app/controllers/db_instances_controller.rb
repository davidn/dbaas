class DbInstancesController < ApplicationController

  def index

  end

  def new
    @db_instance = DbInstance.new
  end

  def create
    @db_instance = DbInstance.new(params[:db_instance])
    debugger
    if @db_instance.save
      redirect_to root_path
    else
      render 'new'
    end
  end

  def edit

  end

  def update

  end

end
