class DbInstancesController < ApplicationController

  def new
		reset_session
		session[:db_params] ||= {}
		@db_instance = DbInstance.new
  end

  def create
		debugger
		session[:db_params].deep_merge!(params[:db_instance]) if params[:db_instance]
    @db_instance = DbInstance.new(session[:db_params])
		@db_instance.current_step = session[:db_step]
		if @db_instance.valid?
			if params[:back_button]
				@db_instance.previous_step
			elsif @db_instance.last_step?
				@db_instance.save
			else
				@db_instance.next_step
			end
		end
		session[:db_step] = @db_instance.current_step
		if @db_instance.new_record?
			render "new"
		else
			session[:db_params] = session[:db_step] = nil
			flash[:notice] = "Instance Saved"
			redirect_to root_path
		end
  end

end
